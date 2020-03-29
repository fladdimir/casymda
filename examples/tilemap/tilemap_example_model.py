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
    TilemapMovement,
)
from examples.tilemap.coordinates_holder_setup import get_coordinates_holder

coordinates_holder = get_coordinates_holder()


class Model:
    """generated model"""

    def __init__(self, env):

        self.env = env

        #!resources+components

        self.source = Source(
            self.env,
            "source",
            xy=(80, 59),
            inter_arrival_time=100,
            max_entities=2,
            ways={"tilemover": [(98, 59), (181, 59)]},
        )

        self.sink = Sink(self.env, "sink", xy=(369, 59), ways={})

        self.tilemover = TilemapMovement(
            self.env,
            "tilemover",
            xy=(231, 59),
            speed=10,
            coordinates_holder=coordinates_holder,
            from_node="A",
            to_node="C",
            ways={"sink": [(281, 59), (351, 59)]},
        )

        #!model

        self.model_components = {
            "source": self.source,
            "sink": self.sink,
            "tilemover": self.tilemover,
        }

        self.model_graph_names = {
            "source": ["tilemover"],
            "sink": [],
            "tilemover": ["sink"],
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
