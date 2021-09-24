"""create a casymda model from a bpmn file and a template"""
from casymda.bpmn.bpmn_parser import parse_bpmn

BPMN_PATH = "examples/wait_for_interrupt/diagram.bpmn"
TEMPLATE_PATH = "examples/wait_for_interrupt/model_template.py"
JSON_PATH = "examples/wait_for_interrupt/_temp_diagram_bpmn.json"
MODEL_PATH = "examples/wait_for_interrupt/model.py"


def test_parse_bpmn():
    """parse_bpmn"""
    parse_bpmn(BPMN_PATH, JSON_PATH, TEMPLATE_PATH, MODEL_PATH)


if __name__ == "__main__":
    test_parse_bpmn()
