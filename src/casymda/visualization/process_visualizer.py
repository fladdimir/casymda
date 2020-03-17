"""process visualizer"""
import datetime
import time
from typing import Dict, List, Tuple

import casymda.visualization.state_icons.state_icons_pathfinder as state_icon_pathfinder
from casymda.blocks.block_components import VisualizableBlock
from casymda.blocks.block_components.state import States
from casymda.blocks.block_components.visualizer_interface import BlockVisualizer
from casymda.visualization.canvas.scaled_canvas import ScaledCanvas
from casymda.visualization.entity_visualizer import EntityVisualizer


class ProcessVisualizer(EntityVisualizer, BlockVisualizer):
    """ visualizes block processes at a given canvas.
        extends EntityVisualizer by BlockVisualizer animation behavior """


    def __init__(
        self,
        canvas: ScaledCanvas,
        flow_speed: float = 200,
        background_image_path: str = "",
        default_entity_icon_path: str = "",
    ):

        self.flow_speed = flow_speed  # speed of entity movement in pixels per second

        super().__init__(canvas, background_image_path, default_entity_icon_path)
        self.block_animations: List[BlockAnimation] = []

    def animate_block(self, block: VisualizableBlock, queuing_direction_x=-20):
        # creates new or updates existing animation
        queuing = block.queuing
        block_anim = self._find_or_create_block_anim(block)

        # update text
        if len(block.entities) > 5:  # don"t provide too much details
            content_list_str = "Entities:  " + str(len(block.entities))
        else:
            content_list_str = "\n".join(
                [
                    " - ".join(
                        [
                            entity.name,
                            str(
                                datetime.timedelta(
                                    seconds=int(entity.time_of_last_arrival)
                                )
                            ),
                        ]
                    )
                    for entity in block.entities
                ]
            )
        self.canvas.set_text_value(block_anim.content_list, text=content_list_str)

        self.updatetime_label(block.env.now)

        # update entity animations as well if they should queue
        if queuing:
            x_coord, y_coord = block.xy_position
            queuing_offset_x = 0
            for entity in block.entities:
                self._animate_flow_x_y(
                    x_coord,
                    y_coord,
                    x_coord + queuing_offset_x,
                    y_coord,
                    entity,
                    skip_flow=True,
                )
                queuing_offset_x += queuing_direction_x

    def animate_entity_flow(
        self, entity, from_block: VisualizableBlock, to_block: VisualizableBlock
    ):

        self.updatetime_label(from_block.env.now)

        if to_block is None:
            self.destroy(entity)  # e.g. at the sink
            return

        ways = from_block.ways
        skip_flow = False  # might be moved to block if interesting

        from_x, from_y = from_block.xy_position
        to_x, to_y = to_block.xy_position

        # if waypoints exist, animate flow between waypoints first and update
        # fx, fy
        if ways is not None and to_block.name in ways:
            for way in from_block.ways[to_block.name]:
                self._animate_flow_x_y(
                    from_x, from_y, *way, entity, skip_flow=skip_flow
                )
                from_x, from_y = way

        self._animate_flow_x_y(from_x, from_y, to_x, to_y, entity, skip_flow=skip_flow)

    def _animate_flow_x_y(self, from_x, from_y, to_x, to_y, entity, skip_flow):
        """ change entity position via optional movement animation """

        # find / create entity animation
        entity_anim = self._find_or_create_entity_animation(entity, from_x, from_y)
        entity_icon = entity_anim.canvas_image

        # make sure starting position is as expected
        self.canvas.set_coords(entity_icon, (from_x, from_y))
        self._move_icon(
            from_x, from_y, to_x, to_y, entity_icon, self.flow_speed, skip_flow
        )

        entity_anim.x_y = (to_x, to_y)  # update known position

    def _move_icon(self, from_x, from_y, to_x, to_y, icon, flow_speed, skip_flow):
        """ only animate flow if not skipped """
        if skip_flow:
            self.canvas.set_coords(icon, (to_x, to_y))
            return

        distance = ((to_x - from_x) ** 2 + (to_y - from_y) ** 2) ** 0.5
        if distance == 0:
            return  # target already reached

        # wallclock time needed for distance
        needed_time = distance / float(flow_speed)
        fps = 30  # aninmations per second
        # distance / number of animations = distance per move
        remaining_x_dist = to_x - from_x
        remaining_y_dist = to_y - from_y
        x_per_frame = (remaining_x_dist) / (needed_time * fps)
        y_per_frame = (remaining_y_dist) / (needed_time * fps)

        # animation loop
        while (abs(remaining_x_dist) + abs(remaining_y_dist)) > 0:
            # do not move further than necessary
            x_move = (
                remaining_x_dist
                if abs(remaining_x_dist) < abs(x_per_frame)
                else x_per_frame
            )
            y_move = (
                remaining_y_dist
                if abs(remaining_y_dist) < abs(y_per_frame)
                else y_per_frame
            )

            remaining_x_dist -= x_move
            remaining_y_dist -= y_move

            current_x = to_x - remaining_x_dist
            current_y = to_y - remaining_y_dist

            self.canvas.set_coords(icon, (current_x, current_y))
            time.sleep(1 / float(fps))  # sleep until next frame

    def create_block_animation(self, block: VisualizableBlock):
        """currently only consists of updated list of entities,
        contents list"s position to slightly below the center"""
        x_coord, y_coord = block.xy_position
        x_coord -= 20
        y_coord += 20
        content_list = self.canvas.create_text(
            x_coord, y_coord, font="Helvetica 10", fill="black", anchor="nw", text="",
        )

        block_animation = BlockAnimation(block, content_list)
        self.block_animations.append(block_animation)
        return block_animation

    def _find_or_create_block_anim(self, block: VisualizableBlock):
        """creates new or updates existing animation"""
        block_animation = next(
            (x for x in self.block_animations if x.block is block), None
        )  # existing
        if block_animation is None:
            block_animation = self.create_block_animation(block)  # new
        return block_animation

    def change_block_state(
        self, block: VisualizableBlock, state: States, new_value: bool
    ):

        block_animation = self._find_or_create_block_anim(block)
        if new_value is True:
            state_icon = StateIcon(
                state.value,
                block.xy_position,
                state_icon_pathfinder.get_file_path(state),
                self.canvas,
            )
            block_animation.state_icons[state.value] = state_icon
        else:
            if state.value in block_animation.state_icons:
                self.canvas.delete(block_animation.state_icons[state.value].icon)
                del block_animation.state_icons[state.value]


class StateIcon:
    """icon to visualize the block's state"""

    OFFSETS: Dict[str, Tuple[int, int]] = {
        States.busy.value: (38, -25),
        States.empty.value: (38, -25),
        States.blocked.value: (38, 0),
    }

    def __init__(
        self,
        state_value: str,
        x_y: Tuple[int, int],
        path_to_icon: str,
        canvas: ScaledCanvas,
    ):
        self.state_value = state_value
        self.x_y: List[int] = list(map(sum, zip(x_y, self.OFFSETS[state_value])))
        self.photo = canvas.load_image_file(path_to_icon)
        self.icon = canvas.create_image(
            self.x_y[0], self.x_y[1], image_file=self.photo, anchor="c"
        )


class BlockAnimation:
    """class to hold block animation"""

    def __init__(self, block, content_list, icon=None, text=None):
        self.block = block
        self.content_list = content_list
        self.icon = icon
        self.text = text
        self.state_icons: Dict[str, StateIcon] = {}
