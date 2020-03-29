"""sink"""
from typing import Optional
from casymda.blocks.block_components import VisualizableBlock
from examples.gym.model.blocks.fruit_entity import FruitEntity
from examples.gym.model.gym_helper import RewardHolder


class FruitSink(VisualizableBlock):
    """sink; yields 0 timeout event before no further processing is started"""

    def __init__(self, env, name, xy=None, ways=None, fruit_type=""):
        super().__init__(env, name, xy=xy, ways=ways)

        self.fruit_type = fruit_type
        self.reward_holder: Optional[RewardHolder] = None

    def process_entity(self, entity: FruitEntity):

        self.check_fruit_type_of_entity(entity)

        yield self.env.timeout(0)

        self.on_enter(entity)
        self.entities.append(entity)
        self.block_resource.release(entity.block_resource_request)
        self.on_exit(entity, None)

    def actual_processing(self, entity):
        """not called in this special block"""

    def check_fruit_type_of_entity(self, entity: FruitEntity):

        if entity.fruit_type == self.fruit_type:
            self.increase_reward_by(1)
        else:
            self.increase_reward_by(-1)

    def increase_reward_by(self, by: float):
        if self.reward_holder is not None:
            self.reward_holder.increase_step_reward(by)
