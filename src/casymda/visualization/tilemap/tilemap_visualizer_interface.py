from casymda.blocks.entity import Entity


class TilemapVisualizerInterface:
    """ interface for tilemap visualizations """

    def animate(self, entity: Entity, x: float, y: float, current_time: float):
        raise NotImplementedError()

    def destroy(self, entity: Entity):
        raise NotImplementedError()
