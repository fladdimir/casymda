"""seize resource"""
from casymda.blocks.block_components import VisualizableBlock
from casymda.blocks import Entity


class ResourceSeizeQueue(VisualizableBlock):
    """waiting for free resource before seizing and moving forward"""

    def __init__(self, env, name, xy=None, ways=None, resource=None):
        super().__init__(env, name, xy=xy, ways=ways)

        self.resource_to_request = resource

    def actual_processing(self, entity: Entity):
        req = self.resource_to_request.request()
        yield req
        entity.seized_resources.append(req)
