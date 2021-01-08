"""calculates and caches information on shortest paths between locations on a tilemap"""
import pickle
from typing import Dict, Any, Tuple

import networkx as nx
from numpy import genfromtxt, vectorize

# left, right, up, down / w, e, n, s (distance 1)
non_diagonal_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
# nw, ne, se, sw (distance 1.41)
diagonal_directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]


def initialize(
    pickled_matrix_path: str,
    pickled_lookup_path: str,
    csv_path: str,
    include_diagonal=False,
) -> Tuple[Dict[Any, Any], Dict[Any, Any]]:
    """load pickled cache if present; create otherwise"""
    matrix_dict, node_lookup = try_to_load_matrix_dict_and_lookup(
        pickled_matrix_path, pickled_lookup_path
    )
    if None in (matrix_dict, node_lookup):
        matrix_dict, node_lookup = prepare_matrix_lookup(
            csv_path,
            pickled_matrix_path,
            pickled_lookup_path,
            include_diagonal=include_diagonal,
        )
    return matrix_dict, node_lookup


def prepare_matrix_lookup(
    csv_path, pickled_matrix_path, pickled_lookup_path, include_diagonal=False
):
    G = get_graph_from_csv(csv_path, include_diagonal=include_diagonal)
    matrix_dict, node_lookup = get_matrix_dict_from_csv(csv_path, G)
    sorted_node_lookup_keys = sorted(list(node_lookup))
    node_lookup = {key: node_lookup[key] for key in sorted_node_lookup_keys}
    pickle_matrix_dict_and_lookup(
        matrix_dict, pickled_matrix_path, node_lookup, pickled_lookup_path
    )
    return matrix_dict, node_lookup


def get_graph_from_csv(csv_path, valid_node_value=0, include_diagonal=False):
    array = _get_0_1_array_from_csv(csv_path)
    G = get_graph_from_tilemap_array(array, valid_node_value, include_diagonal)
    return G


def _get_0_1_array_from_csv(csv_path):
    # all values different from "1" will be marked as passable
    str_array = genfromtxt(csv_path, dtype=str, delimiter=",")
    f = vectorize(lambda x: 1 if x == "1" else 0)
    array_0_1 = f(str_array)
    return array_0_1


def get_graph_from_tilemap_array(array, valid_node_value, include_diagonal=False):

    edgelist = _get_edgelist_from_array(array, valid_node_value, include_diagonal)

    return nx.from_edgelist(edgelist)


def _get_edgelist_from_array(array, valid_node_value, include_diagonal):
    edgelist = _get_edgelist_for_directions(
        array, valid_node_value, non_diagonal_directions, 1
    )
    if include_diagonal:
        edgelist += _get_edgelist_for_directions(
            array, valid_node_value, diagonal_directions, 1.41
        )
    return edgelist


def _get_edgelist_for_directions(array, valid_node_value, directions, weight):
    edgelist = []
    for element in _get_elements_in_array(array):
        if _valid(element, array, valid_node_value):
            edges = _get_edges_for_neighbours(
                element, directions, array, valid_node_value, weight
            )
            edgelist += edges
    return edgelist


def _get_edges_for_neighbours(element, directions, array, valid_node_value, weight):
    edges = []
    row, col = element
    for direction in directions:
        neighbour = tuple(map(sum, zip(element, direction)))
        if _valid(neighbour, array, valid_node_value):
            edges.append((element, neighbour, {"weight": weight}))
    return edges


def _valid(element, array, valid_node_value):
    num_rows, num_cols = array.shape
    row, col = element
    if 0 <= row < num_rows and 0 <= col < num_cols:
        return array[element] == valid_node_value
    else:
        return False


def _get_elements_in_array(array):
    num_rows, num_cols = array.shape
    elements = []
    for row in range(num_rows):
        for col in range(num_cols):
            element = (row, col)
            elements.append(element)
    return elements


# additional method to get complete distance/path dict for all relevant nodes:


def get_matrix_dict_from_csv(csv_path_nodes, graph):
    nodes = get_relevant_nodes_from_csv(csv_path_nodes)
    nodes_list = list(nodes.keys())
    node_lookup_by_name = {value["name"]: key for key, value in nodes.items()}
    matrix_dict = calculate_matrix_dict(graph, nodes_list)
    return matrix_dict, node_lookup_by_name


def get_relevant_nodes_from_csv(csv_path):
    array = genfromtxt(csv_path, dtype=str, delimiter=",")

    relevant_nodes = {}
    for element in _get_elements_in_array(array):
        if len(array[element]) is not 0 and array[element] not in ["0", "1"]:
            relevant_nodes[element] = {"name": array[element]}
    return relevant_nodes


def calculate_matrix_dict(graph, nodes):
    # {from: {to1: {path:[...], length: X}, to2: ...}}
    result = {}
    for source_node in nodes:
        for target_node in [n for n in nodes if n is not source_node]:
            path = nx.astar_path(graph, source_node, target_node)
            length = nx.astar_path_length(graph, source_node, target_node)
            if source_node not in result:
                result[source_node] = {}
            result[source_node][target_node] = {"path": path, "length": length}
    return result


def pickle_matrix_dict_and_lookup(matrix_dict, matrix_path, node_lookup, lookup_path):
    # tuples cannot easily be json-serialized, so we use pickle here
    for path, obj in {matrix_path: matrix_dict, lookup_path: node_lookup}.items():
        with open(path, "wb+") as f:
            pickle.dump(obj, f)


def try_to_load_matrix_dict_and_lookup(matrix_path, lookup_path):
    def load_obj(path):
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None

    return (load_obj(path) for path in (matrix_path, lookup_path))
