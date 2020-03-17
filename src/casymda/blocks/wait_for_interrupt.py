"""wait for interrupt"""
from simpy import Interrupt

from casymda.blocks.block_components import VisualizableBlock


class WaitForInterrupt(VisualizableBlock):
    """processes entities until their process is interrupted"""

    def __init__(self, env, name, xy=None, ways=None):
        super().__init__(env, name, xy=xy, ways=ways)

    # note: entity.current_process might be used for interrupt
    def actual_processing(self, entity):
        try:
            yield self.env.timeout(float("inf"))
        except Interrupt:
            pass
