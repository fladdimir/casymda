""" simulation process and model-specific config """
from multiprocessing import Value

from casymda.environments.realtime_environment import (
    ChangeableFactorRealtimeEnvironment as Environment,
    SyncedFloat,
)
from casymda.visualization.canvas.web_canvas import WebCanvas
from casymda.visualization.process_visualizer import ProcessVisualizer
from casymda.visualization.tilemap.tilemap_visualizer import TilemapVisualizer
import casymda.visualization.web_server.flask_sim_server as flask_sim_server
from casymda.visualization.web_server.sim_controller import RunnableSimulation

from examples.tilemap.tilemap_example_model import Model
import root_dir


class TilemapProcessRunnableSimulation(RunnableSimulation):
    """Runnable simulation of our example model"""

    # single place to configure the width and height of the canvas, also given to browser
    scale = 1.0
    width = 451 * scale
    height = 212 * scale
    flow_speed = 400
    root_file = root_dir.__file__

    def simulate(self, shared_state: dict, should_run: Value, factor: SyncedFloat):

        env = Environment(factor=factor, should_run=should_run)
        model = Model(env)

        canvas = WebCanvas(
            shared_state,
            self.width,
            self.height,
            scale=self.scale,
        )

        visualizer = ProcessVisualizer(
            canvas,
            flow_speed=self.flow_speed,
            background_image_path="examples/tilemap/diagram.png",
            default_entity_icon_path="examples/basics/visualization/simple_entity_icon.png",
        )

        for block in model.model_components.values():
            block.visualizer = visualizer

        while env.peek() < float("inf"):
            model.env.step()

        print("simulation done.\n")


def run_sim_process_animation():
    runnable_sim = TilemapProcessRunnableSimulation()
    flask_sim_server.run_server(runnable_sim)


class TilemapRunnableSimulation(RunnableSimulation):
    """Runnable simulation of our example model"""

    # single place to configure the width and height of the canvas, also given to browser
    scale = 1.2
    width = 240 * scale
    height = 260 * scale
    root_file = root_dir.__file__

    def simulate(self, shared_state: dict, should_run: Value, factor: SyncedFloat):

        env = Environment(factor=factor, should_run=should_run)
        model = Model(env)

        canvas = WebCanvas(
            shared_state,
            self.width,
            self.height,
            scale=self.scale,
        )
        visualizer = TilemapVisualizer(
            canvas,
            background_image_path="examples/tilemap/tilemap-csv_240.png",
            default_entity_icon_path="examples/tilemap/simple_entity_icon.png",
        )

        model.tilemover.tilemap_visualizer = visualizer

        env.run()

        print("simulation done.\n")


def run_sim_tilemap_animation():
    runnable_sim = TilemapRunnableSimulation()
    flask_sim_server.run_server(runnable_sim)
