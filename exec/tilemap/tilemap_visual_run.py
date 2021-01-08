import sys

sys.path.append(".")

from examples.tilemap import tilemap_visualizer_test

if __name__ == "__main__":
    tilemap_visualizer_test.test_visualized_run_tilemap(rt_factor=0.25)
