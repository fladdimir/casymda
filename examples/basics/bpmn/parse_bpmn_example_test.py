"""create a casymda model from a bpmn file and a template"""
from casymda.bpmn.bpmn_parser import parse_bpmn

BPMN_PATH = "examples/basics/bpmn/bpmn_example.bpmn"
TEMPLATE_PATH = "examples/basics/bpmn/bpmn_example_template.py"
JSON_PATH = "examples/basics/bpmn/_temp_bpmn.json"
MODEL_PATH = "examples/basics/model/bpmn_example_model.py"


def test_parse_bpmn():
    """parse_bpmn"""
    parse_bpmn(BPMN_PATH, JSON_PATH, TEMPLATE_PATH, MODEL_PATH)


if __name__ == "__main__":
    test_parse_bpmn()
