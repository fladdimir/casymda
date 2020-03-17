"""model template for generated model files"""
from casymda.blocks import (
    Delay,
    Entity,
    NamedResource,
    ResourceRelease,
    ResourceSeizeQueue,
    RoundRobinGateway,
    SeizeProcessRelease,
    Sink,
    Source,
)
from examples.gym.model.blocks.fruit_sink import FruitSink
from examples.gym.model.blocks.fruit_source import FruitSource
from examples.gym.model.blocks.fruit_sorting_gateway import FruitSortingGateway


class Model:
    """generated model"""

    def __init__(self, env):

        self.env = env

        #!resources+components

        #!model

        # translate model_graph_names into corresponding objects
        self.model_graph = {
            self.model_components[name]: [
                self.model_components[nameSucc]
                for nameSucc in self.model_graph_names[name]
            ]
            for name in self.model_graph_names
        }

        for component in self.model_graph:
            component.successors = self.model_graph[component]
