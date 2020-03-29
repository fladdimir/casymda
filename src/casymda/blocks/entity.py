""" entity """
from typing import List, Optional

from simpy import Environment, Resource


class Entity:
    """ flow object which is moved between components """

    def __init__(self, env: Environment, name: str):
        self.env = env
        self.name = name
        self.current_process = None

        # requested resources, info needed for release
        self.seized_resources: List[Resource] = []
        self.time_of_last_arrival: float = -1

        self.block_resource_request = None

        # optional special icon path, checked by process_visualizer
        self.process_animation_icon_path: Optional[str] = None
