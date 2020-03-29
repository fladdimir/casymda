""" block """
from typing import List, Optional, Callable

from simpy import Environment, Resource

from casymda.blocks.block_components.state import StateManager, States
from casymda.blocks.entity import Entity


class Block:
    """ contains simulation-specific behavior of a basic block """

    def __init__(self, env: Environment, name: str, block_capacity=float("inf")):
        self.name = name
        self.env: Environment = env
        self.overall_count_in = 0
        on_enter_or_exit_method_callable = Callable[
            [Entity, Optional[Block], Optional[Block]], None
        ]
        self.do_on_enter_list: List[on_enter_or_exit_method_callable] = []
        self.do_on_exit_list: List[on_enter_or_exit_method_callable] = []
        self.entities: List[Entity] = []
        self.successors: List[Block] = []
        self.block_resource = Resource(env=env, capacity=block_capacity)
        self.state_manager = StateManager(self.on_block_state_change)

        self.env.process(self.late_state_evaluation())

    def on_enter(self, entity: Entity):
        """on_enter"""
        entity.time_of_last_arrival = self.env.now
        self.overall_count_in += 1
        for method in self.do_on_enter_list:
            method(entity, None, self)

    def on_exit(self: "Block", entity: Entity, successor: "Block"):
        """called when an entities leaves the block"""
        self.entities.remove(entity)
        for method in self.do_on_exit_list:
            method(entity, self, successor)
        self.on_block_change()
        self.on_entity_movement(entity, successor)

    def process_entity(self, entity: Entity):
        """main entry point for entities coming from predecessors"""
        self.on_enter(entity)
        self.entities.append(entity)
        self.on_block_change()

        # processing
        self.state_manager.increment_state_count(States.busy)
        entity.current_process = self.env.process(self.actual_processing(entity))
        yield entity.current_process  # might be used for interrupt

        # wait for successor
        successor = self.find_successor(entity)
        req = successor.block_resource.request()
        self.state_manager.increment_state_count(States.blocked)
        self.state_manager.decrement_state_count(States.busy)
        yield req  # wait until the chosen successor is ready

        # leaving
        self.block_resource.release(entity.block_resource_request)
        entity.block_resource_request = req  # remember to be released

        self.on_exit(entity, successor)
        self.state_manager.decrement_state_count(States.blocked)

        self.env.process(successor.process_entity(entity))

    def find_successor(self, entity: Entity):
        """find next block to send entity to"""
        return self.successors[0]

    def on_block_change(self):
        """called on block change"""

    def on_block_state_change(self, state, new_value):
        """called when state of the block changes"""

    def on_entity_movement(self, entity: Entity, successor: "Block"):
        """called on entity movement from this block to the successor"""

    def late_state_evaluation(self):
        """schedule evaluation on sim start,
        when the visualizer has been loaded"""
        yield self.env.timeout(0)
        self.state_manager.evaluate_state_count()

    def actual_processing(self, entity: Entity):
        """to be implemented"""
        raise NotImplementedError()
