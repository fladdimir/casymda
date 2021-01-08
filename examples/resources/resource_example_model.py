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

        self.resource_1 = NamedResource(
            self.env, "resource_1", xy=(395, 43), capacity=2, ways={}
        )

        self.source = Source(
            self.env,
            "source",
            xy=(31, 169),
            inter_arrival_time=0,
            max_entities=6,
            ways={"wait_for_resource": [(49, 169), (125, 169)]},
        )

        self.sink = Sink(self.env, "sink", xy=(735, 169), ways={})

        self.proc_1 = Delay(
            self.env,
            "proc_1",
            xy=(315, 169),
            process_time=5,
            ways={"proc_2": [(365, 169), (415, 169)]},
        )

        self.proc_2 = Delay(
            self.env,
            "proc_2",
            xy=(465, 169),
            process_time=5,
            ways={"release_resource": [(515, 169), (575, 169)]},
        )

        self.wait_for_resource = ResourceSeizeQueue(
            self.env,
            "wait_for_resource",
            resource=self.resource_1,
            xy=(175, 169),
            ways={"proc_1": [(225, 169), (265, 169)]},
        )

        self.release_resource = ResourceRelease(
            self.env,
            "release_resource",
            resource=self.resource_1,
            xy=(625, 169),
            ways={"sink": [(675, 169), (717, 169)]},
        )

        #!model

        self.model_components = {
            "source": self.source,
            "sink": self.sink,
            "proc_1": self.proc_1,
            "proc_2": self.proc_2,
            "wait_for_resource": self.wait_for_resource,
            "release_resource": self.release_resource,
        }

        self.model_graph_names = {
            "source": ["wait_for_resource"],
            "sink": [],
            "proc_1": ["proc_2"],
            "proc_2": ["release_resource"],
            "wait_for_resource": ["proc_1"],
            "release_resource": ["sink"],
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
