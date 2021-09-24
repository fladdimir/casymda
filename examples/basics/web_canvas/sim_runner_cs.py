""" simulation process and model-specific config """
from multiprocessing import Value

import casymda.visualization.web_server.flask_sim_server as flask_sim_server
import root_dir
from casymda.environments.realtime_environment import (
    ChangeableFactorRealtimeEnvironment as Environment,
)
from casymda.environments.realtime_environment import SyncedFloat
from casymda.visualization.canvas.web_canvas import WebCanvas
from casymda.visualization.process_visualizer import ProcessVisualizer
from casymda.visualization.web_server.sim_controller import RunnableSimulation
from examples.basics.model.bpmn_example_model import Model

SCALE = 1
FLOW_SPEED = 400
MAX_ENTITIES = 6


class ExampleRunnableSimulation(RunnableSimulation):
    """Runnable simulation of our example model"""

    # single place to configure the width and height of the canvas, also given to browser
    width = 800 * SCALE
    height = 400 * SCALE
    root_file = root_dir.__file__

    def simulate(self, shared_state: dict, should_run: Value, factor: SyncedFloat):

        env = Environment(factor=factor, should_run=should_run)
        model = Model(env)
        model.source.max_entities = MAX_ENTITIES

        canvas = WebCanvas(shared_state, self.width, self.height, scale=SCALE)

        visualizer = ProcessVisualizer(
            canvas,
            flow_speed=FLOW_SPEED,
            background_image_path="examples/basics/visualization/bpmn_example.png",
            default_entity_icon_path="examples/basics/visualization/simple_entity_icon.png",
        )

        for block in model.model_components.values():
            block.visualizer = visualizer

        while env.peek() < float("inf"):
            model.env.step()

        print("simulation done.\n")


def run_sim():
    runnable_sim = ExampleRunnableSimulation()
    flask_sim_server.run_server(runnable_sim, port=5002)
