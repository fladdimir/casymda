"""model template for generated model files"""
from casymda.blocks import Sink, Source, WaitForInterrupt

from .interruptor import Interruptor


class Model:
    """generated model"""

    def __init__(self, env):

        self.env = env

        #!resources+components

        self.source = Source(
            self.env,
            "source",
            xy=(55, 59),
            inter_arrival_time=0,
            max_entities=6,
            ways={"wait": [(73, 59), (131, 59)]},
        )

        self.source_2 = Source(
            self.env,
            "source_2",
            xy=(55, 250),
            inter_arrival_time=1,
            max_entities=6,
            ways={"free_wait": [(73, 250), (131, 250)]},
        )

        self.sink = Sink(self.env, "sink", xy=(311, 59), ways={})

        self.sink_2 = Sink(self.env, "sink_2", xy=(311, 250), ways={})

        self.wait = WaitForInterrupt(
            self.env, "wait", xy=(181, 59), ways={"sink": [(231, 59), (293, 59)]}
        )

        self.free_wait = Interruptor(
            self.env,
            "free_wait",
            xy=(181, 250),
            ways={"sink_2": [(231, 250), (293, 250)]},
        )

        #!model

        self.model_components = {
            "source": self.source,
            "source_2": self.source_2,
            "sink": self.sink,
            "sink_2": self.sink_2,
            "wait": self.wait,
            "free_wait": self.free_wait,
        }

        self.model_graph_names = {
            "source": ["wait"],
            "source_2": ["free_wait"],
            "sink": [],
            "sink_2": [],
            "wait": ["sink"],
            "free_wait": ["sink_2"],
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

        # custom additional wiring logic
        # nice possible extension: set this type of link in the bpmn and parse it
        self.free_wait.block_to_interrupt = self.wait
