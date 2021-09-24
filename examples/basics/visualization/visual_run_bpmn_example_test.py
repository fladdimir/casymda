"""simple example including visualization"""
import os
from simpy import Environment
from tkinter import *

from casymda.visualization.process_visualizer import ProcessVisualizer
from casymda.visualization.canvas.tk_canvas import ScaledCanvasTk
from examples.basics.model.bpmn_example_model import Model

FLOW_SPEED = 2 ** 20
MAX_ENTITIES = 2


def test_visualized_run():
    """test visualized run"""
    if os.name != "nt" and os.environ.get("DISPLAY", "") == "":
        print("no display, animated run pointless (e.g. inside a container)")
        # (this check for DISPLAY does not work on win)
        return

    env = Environment()
    model = Model(env)
    model.source.max_entities = MAX_ENTITIES

    width = 800
    height = 600
    gui = Tk()
    canvas = ScaledCanvasTk(gui, width, height)

    visualizer = ProcessVisualizer(
        canvas,
        flow_speed=FLOW_SPEED,
        background_image_path="examples/basics/visualization/bpmn_example.png",
        default_entity_icon_path="examples/basics/visualization/simple_entity_icon.png",
    )

    for block in model.model_components.values():
        block.visualizer = visualizer

    model.env.run(until=float("inf"))

    assert model.sink.overall_count_in == model.source.max_entities == MAX_ENTITIES

    gui.destroy()
