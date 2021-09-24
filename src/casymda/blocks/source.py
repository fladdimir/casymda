"""source"""
from typing import Type

from casymda.blocks.block_components import VisualizableBlock
from casymda.blocks.entity import Entity


class Source(VisualizableBlock):
    """the source has a scheduled "creation_loop" process,
    which creates entities and then processes them regularly
    (as if the entity just entered a regular block,
    but with 0 time delay)"""

    def __init__(
        self,
        env,
        name,
        xy=None,
        ways=None,
        entity_type: Type[Entity] = Entity,
        inter_arrival_time: int = 0,
        max_entities: int = 5,
    ):

        super().__init__(env, name, xy=xy, ways=ways)

        self.entity_type = entity_type
        self.inter_arrival_time = inter_arrival_time
        self.max_entities = max_entities

        self.entity_counter = 0

        self.env.process(self.creation_loop())

    def creation_loop(self):
        """create entities as needed"""
        for i in range(self.max_entities):
            self.entity_counter += 1
            entity = self.entity_type(self.env, "entity_" + str(self.entity_counter))

            entity.block_resource_request = self.block_resource.request()
            yield entity.block_resource_request

            self.env.process(self.process_entity(entity))

            if i < self.max_entities - 1:
                yield self.env.timeout(self.inter_arrival_time)

    def actual_processing(self, entity):
        yield self.env.timeout(0)
