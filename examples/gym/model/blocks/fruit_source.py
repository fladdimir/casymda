"""creates fruits of a given type

fruit-type, e.g.: "apple", "pear"
"""

from casymda.blocks.block_components import VisualizableBlock
from examples.gym.model.blocks.fruit_entity import FruitEntity

MAX_ENTITIES = 100


class FruitSource(VisualizableBlock):
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
        fruit_type: str = "",
        mean_inter_arrival_time: int = 10,
    ):

        super().__init__(env, name, xy=xy, ways=ways)

        self.fruit_type = fruit_type

        self.mean_inter_arrival_time = mean_inter_arrival_time

        self.max_entities = MAX_ENTITIES

        self.entity_counter = 0

        self.env.process(self.creation_loop())

    def creation_loop(self):
        """create entities as needed"""
        for _ in range(self.max_entities):
            self.entity_counter += 1

            entity = FruitEntity(
                self.env,
                self.fruit_type + "_" + str(self.entity_counter),
                self.fruit_type,
            )

            entity.block_resource_request = self.block_resource.request()
            yield entity.block_resource_request

            self.env.process(self.process_entity(entity))

            yield self.env.timeout(self.mean_inter_arrival_time)

    def actual_processing(self, entity):
        yield self.env.timeout(0)
