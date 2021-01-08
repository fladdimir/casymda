"""simple example including visualization"""
import os
from tkinter import Tk

from casymda.environments.realtime_environment import (
    ChangeableFactorRealtimeEnvironment as RealtimeEnvironment,
)

from casymda.visualization.canvas.tk_canvas import ScaledCanvasTk
from casymda.visualization.tilemap.tilemap_visualizer import TilemapVisualizer
from examples.tilemap.tilemap_example_model import Model


def test_visualized_run_tilemap(rt_factor=0.001):
    """test visualized run"""
    if os.name != "nt" and os.environ.get("DISPLAY", "") == "":
        print("no display, animated run pointless (e.g. inside a container)")
        # (this check for DISPLAY does not work on win)
        return

    MAX_ENTITIES = 1

    env = RealtimeEnvironment()
    env.factor.set_value(rt_factor)

    model = Model(env)
    model.source.max_entities = MAX_ENTITIES

    scale = 1.5
    width = 240 * scale
    height = 260 * scale
    gui = Tk()
    canvas = ScaledCanvasTk(gui, width, height, scale=scale)

    visualizer = TilemapVisualizer(
        canvas,
        background_image_path="examples/tilemap/tilemap-csv_240.png",
        default_entity_icon_path="examples/tilemap/simple_entity_icon.png",
    )

    model.tilemover.tilemap_visualizer = visualizer

    model.tilemover.speed = 1

    distance = 17.05 * model.tilemover.coordinates_holder.scale

    estimated_sim_time = distance / model.tilemover.speed

    env.run()

    gui.destroy()

    assert model.sink.overall_count_in == MAX_ENTITIES
    assert model.env.now - estimated_sim_time <= model.tilemover.MAX_ANIMATION_TIMESTEP
