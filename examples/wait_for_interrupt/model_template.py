"""model template for generated model files"""
from casymda.blocks import Sink, Source, WaitForInterrupt

from .interruptor import Interruptor


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

        # custom additional wiring logic
        # nice possible extension: set this type of link in the bpmn and parse it
        self.free_wait.block_to_interrupt = self.wait
