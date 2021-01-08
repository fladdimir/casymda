"""test source"""
from typing import List
from simpy import Environment

from casymda.blocks import Source, Entity
from casymda.blocks.block_components import VisualizableBlock


def test_if_source_is_creating_entities():
    """test source"""
    env = Environment()
    core_source = Source(env, "source", inter_arrival_time=0)
    entity_receiver = EntityReceiver(env)
    core_source.successors.append(entity_receiver)

    env.run(until=1)
    assert len(entity_receiver.received_entities) == core_source.overall_count_in
    assert core_source.overall_count_in == core_source.max_entities


class EntityReceiver(VisualizableBlock):
    """entity receiver"""

    received_entities: List[Entity] = []

    def __init__(self, env):
        super().__init__(env, "name")

    def process_entity(self, entity):
        self.received_entities.append(entity)
        yield self.env.timeout(0)

    def actual_processing(self, entity):
        pass
