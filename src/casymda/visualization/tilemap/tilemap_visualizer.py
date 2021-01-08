"""
2D visualization of positions on a ScaledCanvas
"""

from casymda.visualization.entity_visualizer import EntityVisualizer
from casymda.visualization.tilemap.tilemap_visualizer_interface import (
    TilemapVisualizerInterface,
)


class TilemapVisualizer(EntityVisualizer, TilemapVisualizerInterface):
    """ visualizes entity positions at a given canvas """
