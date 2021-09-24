"""sample model execution"""
import examples.basics.model.bpmn_example_model as model_module
from simpy import Environment


def test_simple_run():
    """run model"""

    env = Environment()
    model = model_module.Model(env)
    model.source.max_entities = 10 ** 3  # increase for higher runtime
    model.source.inter_arrival_time = 0  # increase for lower runtime

    model.env.run()

    assert model.sink.overall_count_in == model.source.overall_count_in
    assert model.sink.overall_count_in == model.source.max_entities

    print("\n\nsimulation done.\n\n")


if __name__ == "__main__":
    test_simple_run()
