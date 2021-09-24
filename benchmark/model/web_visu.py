import sys

sys.path.append(".")

from multiprocessing import Value

import casymda.visualization.web_server.flask_sim_server as flask_sim_server
import root_dir
from benchmark.model.model import Model
from casymda.environments.realtime_environment import (
    ChangeableFactorRealtimeEnvironment as Environment,
)
from casymda.environments.realtime_environment import SyncedFloat
from casymda.visualization.canvas.web_canvas import WebCanvas
from casymda.visualization.process_visualizer import ProcessVisualizer
from casymda.visualization.web_server.sim_controller import RunnableSimulation

SCALE = 1
FLOW_SPEED = 400
MAX_ENTITIES = 10


class ExampleRunnableSimulation(RunnableSimulation):
    """Runnable simulation of our example model"""

    # single place to configure the width and height of the canvas, also given to browser
    width = 622 * SCALE
    height = 341 * SCALE
    root_file = root_dir.__file__

    def simulate(self, shared_state: dict, should_run: Value, factor: SyncedFloat):

        env = Environment(factor=factor, should_run=should_run)
        model = Model(env)
        model.source.max_entities = MAX_ENTITIES

        canvas = WebCanvas(shared_state, self.width, self.height, scale=SCALE)

        visualizer = ProcessVisualizer(
            canvas,
            flow_speed=FLOW_SPEED,
            background_image_path="benchmark/model/diagram.png",
            default_entity_icon_path="benchmark/model/simple_entity_icon.png",
        )

        for block in model.model_components.values():
            block.visualizer = visualizer

        while env.peek() < float("inf"):
            model.env.step()

        print("simulation done.\n")


def run_sim():
    runnable_sim = ExampleRunnableSimulation()
    flask_sim_server.run_server(runnable_sim, port=5000)


if __name__ == "__main__":
    run_sim()
