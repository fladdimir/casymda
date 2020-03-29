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

        self.pear_source = FruitSource(
            self.env,
            "pear_source",
            xy=(65, 263),
            fruit_type="pear",
            ways={"basket": [(83, 263), (164, 263), (164, 173), (215, 173)]},
        )

        self.apple_source = FruitSource(
            self.env,
            "apple_source",
            xy=(65, 83),
            fruit_type="apple",
            ways={"basket": [(83, 83), (164, 83), (164, 173), (215, 173)]},
        )

        self.pear_sink = FruitSink(
            self.env, "pear_sink", xy=(515, 83), fruit_type="pear", ways={}
        )

        self.apple_sink = FruitSink(
            self.env, "apple_sink", xy=(515, 263), fruit_type="apple", ways={}
        )

        self.basket = Delay(
            self.env, "basket", xy=(265, 173), ways={"sorter": [(315, 173), (350, 173)]}
        )

        self.sorter = FruitSortingGateway(
            self.env,
            "sorter",
            xy=(375, 173),
            ways={
                "pear_sink": [(385, 158), (435, 83), (497, 83)],
                "apple_sink": [(385, 188), (435, 263), (497, 263)],
            },
        )

        #!model

        self.model_components = {
            "pear_source": self.pear_source,
            "apple_source": self.apple_source,
            "pear_sink": self.pear_sink,
            "apple_sink": self.apple_sink,
            "basket": self.basket,
            "sorter": self.sorter,
        }

        self.model_graph_names = {
            "pear_source": ["basket"],
            "apple_source": ["basket"],
            "pear_sink": [],
            "apple_sink": [],
            "basket": ["sorter"],
            "sorter": ["pear_sink", "apple_sink"],
        }
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
