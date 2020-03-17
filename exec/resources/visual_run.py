import sys

sys.path.append(".")

from examples.resources import visual_run_resource_example_test


if __name__ == "__main__":
    visual_run_resource_example_test.MAX_ENTITIES = 6
    visual_run_resource_example_test.FLOW_SPEED = 200
    visual_run_resource_example_test.test_visualized_run()
