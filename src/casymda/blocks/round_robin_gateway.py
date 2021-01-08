"""gateway"""
from casymda.blocks.block_components import VisualizableBlock
from casymda.blocks.entity import Entity


class RoundRobinGateway(VisualizableBlock):
    """gateway which cyclically chooses next successor for incoming entities"""

    def __init__(self, env, name, xy=None, ways=None):
        super().__init__(env, name, xy=xy, ways=ways)

        self.round_robin = self.round_robin_generator()

    def actual_processing(self, entity):
        yield self.env.timeout(0)

    def find_successor(self, entity: Entity):
        return next(self.round_robin)

    def round_robin_generator(self):
        """iterate over successors, remember last one"""
        last = -1
        while True:
            last += 1
            last %= len(self.successors)
            yield self.successors[last]
