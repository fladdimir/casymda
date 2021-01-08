from examples.wait_for_interrupt.model import Model
from simpy import Environment


def test_model():
    env = Environment()
    model = Model(env)

    env.run(until=3)

    assert model.source.overall_count_in == 6
    # three of the six produced entities are still waiting:
    assert model.sink.overall_count_in == 3

    assert model.sink_2.overall_count_in == model.source_2.overall_count_in == 3

    env.run(until=6)

    assert model.sink.overall_count_in == model.source.overall_count_in == 6
    assert model.sink_2.overall_count_in == model.source_2.overall_count_in == 6
