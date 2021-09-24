"""create a casymda model from a bpmn file and a template"""
from casymda.bpmn.bpmn_parser import parse_bpmn

BPMN_PATH = "benchmark/model/diagram.bpmn"
TEMPLATE_PATH = "benchmark/model/model_template.py"
JSON_PATH = "benchmark/model/_temp_bpmn.json"
MODEL_PATH = "benchmark/model/model.py"


def test_parse_bpmn():
    parse_bpmn(BPMN_PATH, JSON_PATH, TEMPLATE_PATH, MODEL_PATH)


if __name__ == "__main__":
    test_parse_bpmn()
