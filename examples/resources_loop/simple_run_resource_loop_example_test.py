"""sample model execution"""
from simpy import Environment

import examples.resources_loop.resource_loop_example_model as model_module


def test_simple_run():
    """run model"""

    env = Environment()
    model = model_module.Model(env)
    model.source.max_entities = 6
    model.source.inter_arrival_time = 0

    model.env.run(until=11)
    assert model.sink.overall_count_in == 1

    model.env.run(until=None)

    assert model.source.overall_count_in == model.source.max_entities
    assert model.sink.overall_count_in == model.source.overall_count_in
    assert model.proc_1.overall_count_in == 11
    assert model.proc_2.overall_count_in == 5

    print("\n\nsimulation done.\n\n")
