"""seize process release"""
from casymda.blocks import Delay, NamedResource, ResourceRelease, ResourceSeizeQueue
from casymda.blocks.block_components import VisualizableBlock


class SeizeProcessRelease(VisualizableBlock):
    """entities in this block follow the process:
    request resource, be processed, release resource"""

    def __init__(
        self, env, name, xy=None, ways=None, process_time=1.0, resource_capacity=1
    ):
        super().__init__(env, name, xy=xy, ways=ways)

        self.resource = NamedResource(self.env, "resource", capacity=resource_capacity)

        self.receiver = Receiver(self.env)

        self.seizer = ResourceSeizeQueue(
            env, self.name + "_seizer", resource=self.resource
        )
        self.seizer.successors.append(self.receiver)
        self.processor = Delay(env, self.name + "_processor", process_time=process_time)
        self.processor.successors.append(self.receiver)
        self.releaser = ResourceRelease(
            env, self.name + "_releaser", resource=self.resource
        )
        self.releaser.successors.append(self.receiver)

    def actual_processing(self, entity):
        yield self.env.process(self.seizer.process_entity(entity))
        yield self.env.process(self.processor.process_entity(entity))
        yield self.env.process(self.releaser.process_entity(entity))


class Receiver:
    """receiver class to act as successor for inner blocks"""

    def __init__(self, env):
        self.env = env
        self.block_resource = NamedResource(env, "receiver_resource", capacity=1)

    def process_entity(self, entity):
        """just release the resource"""
        yield self.block_resource.release(entity.block_resource_request)
