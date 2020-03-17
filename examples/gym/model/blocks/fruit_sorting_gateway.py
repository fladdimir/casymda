"""gateway"""
from typing import Optional
from casymda.blocks.entity import Entity
from simpy import Event
from casymda.blocks.block_components import VisualizableBlock
from examples.gym.model.gym_helper import ActionHolder


class FruitSortingGateway(VisualizableBlock):
    """gateway which sorts incoming entities"""

    def __init__(self, env, name, xy=None, ways=None):
        super().__init__(env, name, xy=xy, ways=ways, block_capacity=1)
        # (this block only processes one entity at a time)

        self.decision = 0

        self.action_holder: Optional[ActionHolder] = None

    def actual_processing(self, entity):
        # action needed

        if self.action_holder is not None:
            self.action_holder.provided_action = Event(self.env)

            # this way the gym_env can run the simulation until an action is needed
            self.action_holder.action_needed.succeed()

            # consume provided action
            action = yield self.action_holder.provided_action
            self.decision = action

        else:
            yield self.env.timeout(0)

    def find_successor(self, entity: Entity):
        return self.successors[self.decision]
