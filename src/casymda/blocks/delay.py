""" process """
from casymda.blocks.block_components import VisualizableBlock


# processed entity waits for process time (timeout) before being forwarded
# to the successor


class Delay(VisualizableBlock):
    """simple delay for a given time"""

    def __init__(self, env, name, xy=None, ways=None, process_time=1.0):
        super().__init__(env, name, xy=xy, ways=ways)
        self.process_time = process_time

    def actual_processing(self, entity):
        yield self.env.timeout(self.process_time)
