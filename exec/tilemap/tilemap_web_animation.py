import sys

sys.path.append(".")

from examples.tilemap.web_animation.sim_runner_cs import (
    run_sim_tilemap_animation as action,
)

if __name__ == "__main__":
    action()
