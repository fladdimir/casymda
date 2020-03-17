"""bpmn parser"""
import json
import pathlib
from operator import sub
from typing import Dict, List

import black
import xmltodict

from casymda import __version__

print("casymda version: " + __version__)

OFFSET_REDUCTION = (5, 3)

MAPPING = {
    "dataStoreReference": "resources",
    "startEvent": "sources",
    "endEvent": "sinks",
    "task": "tasks",
    "exclusiveGateway": "xGateways",
    "sequenceFlow": "connectors",
    "textAnnotation": "textAnnotations",
    "association": "associations",
}

COMPONENTS = ["sources", "sinks", "tasks", "xGateways"]


def parse_bpmn(
    bpmn_path: str, json_path: str, template_path: str, model_path: str
) -> None:
    """this module reads from a given bpmn/xml file and
    completes a given skeleton template by initialized blocks and
    their order"""

    bpmn = _to_json_dict(bpmn_path, json_path)

    elements = {
        value: _get_elements_of_type(bpmn, key) for key, value in MAPPING.items()
    }

    components = _get_components_from_elements(elements)

    _add_class_and_id_names(components + elements["resources"])

    insertions = _generate_insertions(bpmn, elements, components)
    model_components = _generate_model_components(components)
    model_graph_names = _generate_model_graph_names(elements, components)

    _write_model_file(
        model_path, template_path, insertions, model_components, model_graph_names
    )

    path = pathlib.Path(model_path)
    file_mode = black.FileMode()
    black.format_file_in_place(path, False, file_mode, write_back=black.WriteBack.YES)

    print("\nBPMN parsed.\n")


def _generate_model_components(components):
    return (
        "self.model_components = {"
        + ", ".join(
            [
                "'" + comp["id_name"] + "': self." + comp["id_name"]
                for comp in components
            ]
        )
        + "}"
    )


def _generate_model_graph_names(elements, components):
    return {
        comp["id_name"]: _get_successor_names_list(comp, elements, components)
        for comp in components
        if not (_get_successor_names_list(comp, elements, components) is None)
    }


def _add_class_and_id_names(elements: list):
    for element in elements:
        names = element["@name"].split(":")
        # add removal of possibly leading/trailing blanks
        names = [n.strip() for n in names]
        element["class_name"] = names[0]
        element["id_name"] = names[1]


def _get_components_from_elements(elements: Dict[str, List[str]]) -> List[str]:
    components: List[str] = []
    for component_label in COMPONENTS:
        components += elements[component_label]
    return components


def _generate_insertions(bpmn, elements, components):
    insertions = []
    offset = _get_offset(bpmn)
    for comp in elements["resources"] + components:
        class_name = comp["class_name"]
        id_name = comp["id_name"]

        x_y = _get_shape_xy(comp["@id"], bpmn, offset=offset)

        res_name = _get_related_resource_id_name(comp, elements)

        if res_name is None:
            insertions.append(
                "self.%s = %s(self.env, '%s', xy=%s"
                % (id_name, class_name, id_name, x_y)
            )
        else:
            insertions.append(
                "self.%s = %s(self.env, '%s', resource=self.%s, xy=%s"
                % (id_name, class_name, id_name, res_name, x_y)
            )

        insertions[-1] += _get_related_text_annotations(comp, elements)

        insertions[-1] += ", ways=" + str(
            _get_ways_to_successors(comp, bpmn, elements, components, offset=offset)
        )

        # close bracket and 2x newline
        insertions[-1] += ")\n\n"
    return insertions


def _write_model_file(
    model_path, template_path, insertions, model_components, model_graph_names
):
    # read template file
    with open(template_path, "r") as template_file:
        template = template_file.readlines()

    loc = 0

    # find resources+components insertion space
    for idx, line in enumerate(template):
        if "#!resources+components" in line:
            loc = idx + 1
            template.insert(loc, "\n")
            break

    for i_line in insertions:
        loc += 1
        template.insert(loc, "".join([" " for _ in range(8)]) + i_line)

    # find #!model insertion space
    for idx, line in enumerate(template):
        if "#!model" in line:
            loc = idx
            break

    loc += 1
    template.insert(loc, "\n" + "".join([" " for _ in range(8)]) + model_components)
    loc += 1
    template.insert(
        loc,
        "\n\n"
        + "".join([" " for _ in range(8)])
        + "self.model_graph_names = "
        + json.dumps(model_graph_names),
    )

    with open(model_path, "w+") as model_file:
        model_file.writelines(template)


def _to_json_dict(bpmn_path: str, json_path: str) -> dict:
    """save bpmn xml as json and return dictionary"""
    with open(bpmn_path, "rb") as bpmn_file:
        bpmn: dict = xmltodict.parse(bpmn_file)
        bpmn = json.loads(json.dumps(bpmn, indent=4))
    with open(json_path, "w+") as json_file:
        json.dump(bpmn, json_file, indent=4)
    return bpmn


def _get_offset(xmlo):
    offset = [float("inf"), float("inf")]

    coords_list = []

    for shape in xmlo["bpmn:definitions"]["bpmndi:BPMNDiagram"]["bpmndi:BPMNPlane"][
        "bpmndi:BPMNShape"
    ]:
        # find all bounded elements and include their label bounds
        shape_bounds = [shape["dc:Bounds"]]
        if "bpmndi:BPMNLabel" in shape:
            shape_bounds.append(shape["bpmndi:BPMNLabel"]["dc:Bounds"])
        for bounds in shape_bounds:
            # look for global min
            coords_list.append((float(bounds["@x"]), float(bounds["@y"])))

    for edge in xmlo["bpmn:definitions"]["bpmndi:BPMNDiagram"]["bpmndi:BPMNPlane"][
        "bpmndi:BPMNEdge"
    ]:
        for waypoint in edge["di:waypoint"]:
            coords_list.append((float(waypoint["@x"]), float(waypoint["@y"])))

    for coords in coords_list:
        for idx, val in enumerate(offset):
            if coords[idx] < val:
                offset[idx] = int(coords[idx])

    offset = tuple(map(sub, offset, OFFSET_REDUCTION))

    return offset


def _get_shape_xy(elid, xmlo, offset=(0, 0)):
    """find position of a shape by element id"""
    for shape in xmlo["bpmn:definitions"]["bpmndi:BPMNDiagram"]["bpmndi:BPMNPlane"][
        "bpmndi:BPMNShape"
    ]:
        if shape["@bpmnElement"] == elid:
            x_y = [
                float(shape["dc:Bounds"]["@x"])
                + int(float(shape["dc:Bounds"]["@width"]) / 2),
                float(shape["dc:Bounds"]["@y"])
                + int(float(shape["dc:Bounds"]["@height"]) / 2),
            ]
            x_y = tuple(map(int, map(sub, x_y, offset)))
            return x_y
    return None


def _get_elements_of_type(bpmn, element_type) -> List[str]:
    process = bpmn["bpmn:definitions"]["bpmn:process"]
    if "bpmn:" + element_type in process:
        elements = process["bpmn:" + element_type]
        return elements if isinstance(elements, list) else [elements]
    return []


def _contains_resource_relation(component):
    if ("bpmn:dataInputAssociation" in component) or (
        "bpmn:dataOutputAssociation" in component
    ):
        return True
    return False


def _find_res_id_name(bpmn_id, elements):
    for res in elements["resources"]:
        if res["@id"] == bpmn_id:
            return res["id_name"]
    return None


def _get_related_resource_id_name(component, elements):
    if "bpmn:dataInputAssociation" in component:
        bpmn_id = component["bpmn:dataInputAssociation"]["bpmn:sourceRef"]
        return _find_res_id_name(bpmn_id, elements)
    if "bpmn:dataOutputAssociation" in component:
        bpmn_id = component["bpmn:dataOutputAssociation"]["bpmn:targetRef"]
        return _find_res_id_name(bpmn_id, elements)
    return None


def _get_related_text_annotations(component, elements):
    associations = [
        assoc
        for assoc in elements["associations"]
        if assoc["@sourceRef"] == component["@id"]
    ]
    # get corresponding textAnnotations
    annotations = []
    for assoc in associations:
        annotations += [
            annot
            for annot in elements["textAnnotations"]
            if annot["@id"] == assoc["@targetRef"]
        ]
    params = []
    for annot in annotations:
        params += [x.strip() for x in annot["bpmn:text"].split(";")]
    text = ""
    if len(params) > 0:
        text = ", " + ", ".join(params)
    return text


def _get_outgoing_sequence_flows(comp):
    # get list of outgoing sequence flows
    if "bpmn:outgoing" not in comp:
        return None
    outgoing_sfs = comp["bpmn:outgoing"]
    outgoing_sfs = (
        [outgoing_sfs] if not isinstance(outgoing_sfs, list) else outgoing_sfs
    )
    return outgoing_sfs


def _get_successor_names_list(comp, elements, components):
    outgoing_sfs = _get_outgoing_sequence_flows(comp)
    res = []
    if outgoing_sfs is None:
        return res
    for seq_flow in outgoing_sfs:
        # find SF element -> find targetRef -> append id_name
        for con in elements["connectors"]:
            if con["@id"] == seq_flow:
                target_id = con["@targetRef"]
                for target_comp in components:
                    if target_comp["@id"] == target_id:
                        res.append(target_comp["id_name"])
                        break
                break
    return res


def _get_diagram_waypoints_for_sf_id(sf_id, xmlo, offset=(0, 0)):
    waypoints = []
    for edge in xmlo["bpmn:definitions"]["bpmndi:BPMNDiagram"]["bpmndi:BPMNPlane"][
        "bpmndi:BPMNEdge"
    ]:
        if edge["@bpmnElement"] == sf_id:
            for waypoint in edge["di:waypoint"]:
                waypoints.append(
                    tuple(
                        map(
                            sub,
                            (int(float(waypoint["@x"])), int(float(waypoint["@y"]))),
                            offset,
                        )
                    )
                )
            return waypoints
    return None


def _get_ways_to_successors(comp, xmlo, elements, components, offset=(0, 0)):
    results = {}  # {"suc name":[{x: int, y: int}, ...]}
    outgoing_sfs = _get_outgoing_sequence_flows(comp)
    if outgoing_sfs is not None:
        for seq_flow in outgoing_sfs:
            # find SF element -> find targetRef -> append id_name: waypoints
            for con in elements["connectors"]:
                if con["@id"] == seq_flow:
                    target_id = con["@targetRef"]
                    for target_comp in components:
                        if target_comp["@id"] == target_id:
                            waypoints = _get_diagram_waypoints_for_sf_id(
                                con["@id"], xmlo, offset=offset
                            )
                            # [{x: int, y: int}]
                            results[target_comp["id_name"]] = waypoints
                            break
                    break
    return results
