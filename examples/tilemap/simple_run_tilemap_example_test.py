"""sample model execution"""
from simpy import Environment

import examples.tilemap.tilemap_example_model as model_module
from examples.tilemap.coordinates_holder_setup import SCALE


def test_simple_run():
    """run model"""

    env = Environment()
    model = model_module.Model(env)
    model.source.max_entities = 1
    model.source.inter_arrival_time = 0
    model.tilemover.speed = 1

    env.run()

    assert model.sink.overall_count_in == 1
    assert env.now == 17.05 * SCALE  # depends on scale: 17.05 * tilemap_scale

    print("\n\nsimulation done.\n\n")
