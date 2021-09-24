import benchmark.model.model as model_module
from simpy import Environment


def test_simple_run():

    model = model_module.Model(Environment())

    model.source.max_entities = 10
    model.source.inter_arrival_time = 0

    model.parallel_proc.process_time = 10
    model.sequential_proc.process_time = 10

    model.env.run()

    assert model.sink.overall_count_in == model.source.overall_count_in
    assert model.parallel_proc.overall_count_in == model.source.max_entities / 2
    assert model.sequential_proc.overall_count_in == model.source.max_entities / 2
    assert model.env.now == 50
