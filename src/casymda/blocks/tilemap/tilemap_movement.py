"""
Simulates and animates tilemap movements from a start node to a target node,
either in one timestep (no visualizer set),
or in steps of a configurable length (visualizer set).
"""
import math
import operator
from typing import Any, List, Optional
from casymda.environments.realtime_environment import (
    ChangeableFactorRealtimeEnvironment,
)

import simpy
from simpy import RealtimeEnvironment

from casymda.blocks.block_components import VisualizableBlock
from casymda.blocks.tilemap.coordinates_holder import CoordinatesHolder
from casymda.blocks.tilemap.segment import Segment
from casymda.visualization.tilemap.tilemap_visualizer_interface import (
    TilemapVisualizerInterface as TilemapVisualizer,
)


class TilemapMovement(VisualizableBlock):

    MAX_ANIMATION_TIMESTEP = 0.1

    def __init__(
        self,
        env,
        name,
        xy=None,
        speed=1,  # px / sec (sim-time)
        coordinates_holder=None,
        from_node="",
        to_node="",
        ways={},
    ):
        super().__init__(env, name, xy=xy, ways=ways)

        self.speed = speed
        if coordinates_holder is None:
            raise Exception("coordinates holder not set in block: " + name)
        self.coordinates_holder: CoordinatesHolder = coordinates_holder
        self.from_node = from_node
        self.to_node = to_node

        self.tilemap_visualizer: Optional[TilemapVisualizer] = None

    def actual_processing(self, entity):
        (
            path_coords,
            overall_length,
        ) = self.coordinates_holder.get_path_coords_and_length_from_to(
            self.from_node, self.to_node
        )

        animation_loop: Any = None
        if self.tilemap_visualizer is not None:
            animation_loop = self.env.process(self.animation_loop(entity, path_coords))

        time_needed = overall_length / self.speed
        yield self.env.timeout(time_needed)

        if self.tilemap_visualizer is not None:
            animation_loop.interrupt()

    # ...animation-related stuff down here:

    def animation_loop(self, entity, path_coords, destroy_on_arrival: bool = True):
        self.tilemap_visualizer.destroy(entity)  # recreate possibly existing animations
        segments = self.get_segments(path_coords)
        time_spent = 0
        # while not interupted
        try:
            while True:
                self.calc_progress_and_animate(entity, segments, time_spent)

                self.set_animation_timestep()
                yield self.env.timeout(self.MAX_ANIMATION_TIMESTEP)
                time_spent += self.MAX_ANIMATION_TIMESTEP
        except simpy.Interrupt:
            """looks like we arrived"""
            x, y = path_coords[-1]
            self.tilemap_visualizer.animate(entity, x, y, self.env.now)
            if destroy_on_arrival:
                self.tilemap_visualizer.destroy(entity)

    def calc_progress_and_animate(self, entity, segments: List[Segment], time_spent):
        distance = self.speed * time_spent
        current_segment = segments[-1]
        for segment in segments:
            current_segment = segment
            if segment.cumulated_length > distance:
                break
        remaining_length = max(current_segment.cumulated_length - distance, 0)
        current_length = current_segment.length - remaining_length
        progress = (
            (
                tuple(
                    map(
                        lambda x: x * (current_length / current_segment.length),
                        current_segment.direction,
                    )
                )
            )
            if current_segment.length > 0
            else current_segment.direction
        )
        current_position = tuple(map(operator.add, progress, current_segment.origin))
        x, y = current_position
        self.tilemap_visualizer.animate(entity, x, y, self.env.now)

    def set_animation_timestep(self):
        if isinstance(self.env, ChangeableFactorRealtimeEnvironment) or isinstance(
            self.env, RealtimeEnvironment
        ):
            self.MAX_ANIMATION_TIMESTEP = 0.04 / self.env.factor
            # keep reference to the factor -> change animation timestep dynamically, if visualized, for a smooth dynamic animation

    def get_segments(self, path_coords):
        """pre-compute needed segment information"""
        segments = []
        cumulated_length = 0
        cumulated_time = 0
        for pc_idx in range(len(path_coords) - 1):
            origin = path_coords[pc_idx]
            destination = path_coords[pc_idx + 1]
            direction = tuple(map(operator.sub, destination, origin))
            squared = map((lambda x: x ** 2), direction)
            length = math.sqrt(sum(squared))
            time_needed = length / self.speed

            cumulated_length += length
            cumulated_time += time_needed

            segment = Segment(
                origin, destination, direction, length, cumulated_length, cumulated_time
            )
            segments.append(segment)
        return segments
