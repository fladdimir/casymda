import sys

sys.path.append(".")

from examples.gym.model import test_visual_run_gym_model


if __name__ == "__main__":
    test_visual_run_gym_model.MAX_ENTITIES = 10
    test_visual_run_gym_model.FLOW_SPEED = 400
    test_visual_run_gym_model.test_visualized_run()
