"""Manages info about shortest paths between certain locations from a given csv tilemap"""
import os
import random
from typing import Any, Dict

import casymda.blocks.tilemap.tilemap_nx as tmnx

MATRIX_CACHE = "_temp_matrix.pickle"
LOOKUP_CACHE = "_temp_lookup.pickle"


def delete_cached(csv_path):
    paths = get_cache_paths(csv_path)
    for path in paths:
        if os.path.exists(path):
            os.remove(path)
            print("removed: " + path)
        else:
            print(path + " does not exist")


def get_cache_paths(csv_path: str):
    cache_directory = os.path.dirname(csv_path)
    pickled_matrix_path = os.path.join(cache_directory, MATRIX_CACHE)
    pickled_lookup_path = os.path.join(cache_directory, LOOKUP_CACHE)
    return pickled_matrix_path, pickled_lookup_path


class CoordinatesHolder:
    def __init__(self, csv_path: str, scale=10, include_diagonal=False) -> None:

        self.csv_path = csv_path
        self.cache_directory = os.path.dirname(csv_path)

        self.pickled_matrix_path, self.pickled_lookup_path = get_cache_paths(csv_path)

        self.scale = scale  # px / tile

        # let info get loaded by tmnx
        self.matrix_dict: Dict[Any, Any]
        self.node_lookup: Dict[Any, Any]
        self.matrix_dict, self.node_lookup = tmnx.initialize(
            self.pickled_matrix_path,
            self.pickled_lookup_path,
            self.csv_path,
            include_diagonal=include_diagonal,
        )

    def get_coords(self, target_name):
        return self.tile_to_coords(self.node_lookup[target_name])

    def get_path_coords_and_length_from_to(self, source_name, target_name):
        if source_name == target_name:
            return [self.get_coords(source_name), self.get_coords(target_name)], 0
        source, target = self.node_lookup[source_name], self.node_lookup[target_name]
        path_nodes = self.matrix_dict[source][target]["path"]
        coords_path = [self.tile_to_coords(tile) for tile in path_nodes]
        length = self.matrix_dict[source][target]["length"] * self.scale
        return coords_path, length

    def get_random_location_name(self):
        i = random.randint(0, len(self.node_lookup) - 1)
        return self.get_location_name_by_index(i)

    def get_location_name_by_index(self, index):
        return list(self.node_lookup)[index]

    def get_location_index_by_name(self, location_name):
        return list(self.node_lookup).index(location_name)

    def tile_to_coords(self, tile_tuple):
        scaled = [(c * self.scale + self.scale / 2) for c in tile_tuple]
        scaled.reverse()  # row, col => y, x
        return tuple(scaled)
