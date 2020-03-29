"""resource release"""
from simpy import Resource

from casymda.blocks.block_components import VisualizableBlock
from casymda.blocks.entity import Entity


class ResourceRelease(VisualizableBlock):
    """releases the specified resource
    (needs to be present in the entities resources list)"""

    def __init__(
        self, env, name, xy=None, ways=None, resource: Resource = None,
    ):
        super().__init__(env, name, xy=xy, ways=ways)

        self.resource_to_release: Resource = resource

    def actual_processing(self, entity: Entity):

        # find request of defined resource in entity requests list
        idx = list(map(lambda x: x.resource, entity.seized_resources)).index(
            self.resource_to_release
        )
        req = entity.seized_resources[idx]

        # done immediately, but necessary for generator behavior
        yield self.resource_to_release.release(req)
