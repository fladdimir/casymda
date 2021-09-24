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

        self.source = Source(
            self.env,
            "source",
            xy=(31, 65),
            inter_arrival_time=0,
            max_entities=10,
            ways={"gateway_1": [(49, 65), (108, 65)]},
        )

        self.sink = Sink(self.env, "sink", xy=(565, 65), ways={})

        self.parallel_proc = Delay(
            self.env,
            "parallel_proc",
            xy=(289, 65),
            process_time=1,
            block_capacity=float("inf"),
            ways={"gateway_2": [(339, 65), (422, 65)]},
        )

        self.sequential_proc = Delay(
            self.env,
            "sequential_proc",
            xy=(355, 229),
            process_time=1,
            block_capacity=1,
            ways={"gateway_2": [(405, 229), (447, 229), (447, 90)]},
        )

        self.buffer = Delay(
            self.env,
            "buffer",
            xy=(215, 229),
            process_time=0,
            block_capacity=float("inf"),
            ways={"sequential_proc": [(265, 229), (305, 229)]},
        )

        self.gateway_1 = RoundRobinGateway(
            self.env,
            "gateway_1",
            xy=(133, 65),
            ways={
                "parallel_proc": [(158, 65), (239, 65)],
                "buffer": [(133, 90), (133, 229), (165, 229)],
            },
        )

        self.gateway_2 = RoundRobinGateway(
            self.env, "gateway_2", xy=(447, 65), ways={"sink": [(472, 65), (547, 65)]}
        )

        #!model

        self.model_components = {
            "source": self.source,
            "sink": self.sink,
            "parallel_proc": self.parallel_proc,
            "sequential_proc": self.sequential_proc,
            "buffer": self.buffer,
            "gateway_1": self.gateway_1,
            "gateway_2": self.gateway_2,
        }

        self.model_graph_names = {
            "source": ["gateway_1"],
            "sink": [],
            "parallel_proc": ["gateway_2"],
            "sequential_proc": ["gateway_2"],
            "buffer": ["sequential_proc"],
            "gateway_1": ["parallel_proc", "buffer"],
            "gateway_2": ["sink"],
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
