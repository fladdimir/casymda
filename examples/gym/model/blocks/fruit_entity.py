""" entity """
import os
from simpy import Environment
from casymda.blocks.entity import Entity

module_dir = os.path.dirname(os.path.abspath(__file__))


class FruitEntity(Entity):
    """ fruit object of a given type which is moved between components """

    def __init__(self, env: Environment, name: str, fruit_type: str):
        super().__init__(env, name)

        self.fruit_type = fruit_type

        # expect icon to be right next to this class
        self.process_animation_icon_path = module_dir + "/" + self.fruit_type + ".png"
