"""sink"""
from casymda.blocks.block_components import VisualizableBlock


class Sink(VisualizableBlock):
    """sink; yields 0 timeout event before no further processing is started"""

    def __init__(self, env, name, xy=None, ways=None):
        super().__init__(env, name, xy=xy, ways=ways)

    def process_entity(self, entity):
        yield self.env.timeout(0)

        self.on_enter(entity)
        self.entities.append(entity)
        self.block_resource.release(entity.block_resource_request)
        self.on_exit(entity, None)

    def actual_processing(self, entity):
        """not called in this special block"""
