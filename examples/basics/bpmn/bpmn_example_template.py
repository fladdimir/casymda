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
