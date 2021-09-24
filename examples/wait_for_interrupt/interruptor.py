from typing import Optional

from casymda.blocks.block_components import VisualizableBlock
from casymda.blocks.block_components.block import Block


class Interruptor(VisualizableBlock):
    """Interrupts the last entity in a linked block, if possible"""

    def __init__(self, env, name, xy=None, ways=None):
        super().__init__(env, name, xy=xy, ways=ways)
        self.block_to_interrupt: Optional[Block] = None

    def actual_processing(self, entity):
        yield self.env.timeout(0)

        if (
            self.block_to_interrupt is not None  # block is set
            and len(self.block_to_interrupt.entities)
            > 0  # block has entities which are currently waiting to be interrupted
        ):
            # find entity to interrupt
            entity_to_interrupt = self.block_to_interrupt.entities[-1]
            entity_to_interrupt.current_process.interrupt()
            print(
                f"{self.name}-{entity.name} interrupted {self.block_to_interrupt.name}-{entity_to_interrupt.name}"
            )
        else:
            print(f"nothing to interrupt for {entity.name}")
