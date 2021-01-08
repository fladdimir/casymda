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
            max_entities=6,
            ways={"gateway_1": [(49, 65), (108, 65)]},
        )

        self.sink = Sink(self.env, "sink", xy=(600, 65), ways={})

        self.spr_1 = SeizeProcessRelease(
            self.env,
            "spr_1",
            xy=(289, 65),
            process_time=41,
            ways={"gateway_2": [(339, 65), (422, 65)]},
        )

        self.proc_1 = Delay(
            self.env,
            "proc_1",
            xy=(289, 186),
            process_time=120,
            ways={"gateway_2": [(339, 186), (447, 186), (447, 90)]},
        )

        self.gateway_1 = RoundRobinGateway(
            self.env,
            "gateway_1",
            xy=(133, 65),
            ways={
                "spr_1": [(158, 65), (239, 65)],
                "proc_1": [(133, 90), (133, 186), (239, 186)],
            },
        )

        self.gateway_2 = RoundRobinGateway(
            self.env, "gateway_2", xy=(447, 65), ways={"sink": [(472, 65), (582, 65)]}
        )

        #!model

        self.model_components = {
            "source": self.source,
            "sink": self.sink,
            "spr_1": self.spr_1,
            "proc_1": self.proc_1,
            "gateway_1": self.gateway_1,
            "gateway_2": self.gateway_2,
        }

        self.model_graph_names = {
            "source": ["gateway_1"],
            "sink": [],
            "spr_1": ["gateway_2"],
            "proc_1": ["gateway_2"],
            "gateway_1": ["spr_1", "proc_1"],
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
