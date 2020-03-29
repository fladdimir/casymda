"""create a casymda model from a bpmn file and a template"""
from casymda.bpmn.bpmn_parser import parse_bpmn

BPMN_PATH = "examples/resources/resource_example.bpmn"
TEMPLATE_PATH = "examples/resources/resource_example_template.py"
JSON_PATH = "examples/resources/_temp_bpmn.json"
MODEL_PATH = "examples/resources/resource_example_model.py"


def test_parse_bpmn():
    """parse_bpmn"""
    parse_bpmn(BPMN_PATH, JSON_PATH, TEMPLATE_PATH, MODEL_PATH)


if __name__ == "__main__":
    test_parse_bpmn()
