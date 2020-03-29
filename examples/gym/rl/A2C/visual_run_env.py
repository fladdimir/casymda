from examples.gym.model.test_visual_run_gym_model import FLOW_SPEED
from tkinter import Tk

from casymda.visualization.canvas.tk_canvas import ScaledCanvasTk
from casymda.visualization.process_visualizer import ProcessVisualizer
from stable_baselines import PPO2
from stable_baselines.common.vec_env import DummyVecEnv

from examples.gym.env import FruitSimEnv
from examples.gym.model.gym_example_model import Model

from examples.gym.rl.A2C.stable_baselines_training import SAVE_NAME

FLOW_SPEED = 400

TOTAL_TIMESTEPS = 25000


def visual_run_env():

    env = FruitSimEnv()
    env = DummyVecEnv(
        [lambda: env]
    )  # The algorithms require a vectorized environment to run

    model = PPO2.load(SAVE_NAME)

    obs = env.reset()

    sim_model = env.envs[0].model
    provide_visualizer_for_model(sim_model)

    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)

    print("done")


def provide_visualizer_for_model(model: Model):
    width = 800
    height = 600
    gui = Tk()
    canvas = ScaledCanvasTk(gui, width, height)

    visualizer = ProcessVisualizer(
        canvas,
        flow_speed=FLOW_SPEED,
        background_image_path="examples/gym/model/gym_example.png",
        default_entity_icon_path="examples/basics/visualization/simple_entity_icon.png",
    )

    for block in model.model_components.values():
        block.visualizer = visualizer
