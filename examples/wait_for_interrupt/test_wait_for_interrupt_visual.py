import os
from tkinter import *

from casymda.visualization.canvas.tk_canvas import ScaledCanvasTk
from casymda.visualization.process_visualizer import ProcessVisualizer
from examples.wait_for_interrupt.model import Model
from simpy import Environment

FLOW_SPEED = 2 ** 20


def test_visualized_run():
    if os.name != "nt" and os.environ.get("DISPLAY", "") == "":
        print("no display, animated run pointless (e.g. inside a container)")
        return

    env = Environment()
    model = Model(env)

    width = 336
    height = 331
    gui = Tk()
    canvas = ScaledCanvasTk(gui, width, height)

    visualizer = ProcessVisualizer(
        canvas,
        flow_speed=FLOW_SPEED,
        background_image_path="examples/wait_for_interrupt/diagram.png",
        default_entity_icon_path="examples/basics/visualization/simple_entity_icon.png",
    )

    for block in model.model_components.values():
        block.visualizer = visualizer

    model.env.run()

    assert model.sink.overall_count_in == model.source.max_entities
    assert model.sink_2.overall_count_in == model.source_2.max_entities

    gui.destroy()
