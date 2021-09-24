"""runs simulation model in its own process"""

import json
from ctypes import c_bool
from multiprocessing import Manager, Process, Value
from typing import Optional

from casymda.environments.realtime_environment import SyncedFloat
from casymda.visualization.canvas import web_canvas

from .flatbuffers import flatbuffer_serializer


class RunnableSimulation:
    """abstract base class for simulations to be run via a SimController"""

    width: int
    height: int
    root_file: str

    def simulate(
        self, shared_state: dict, should_run: Value, factor: SyncedFloat
    ) -> None:
        raise NotImplementedError("abc")


class SimController:
    """wraps RunnableSimulation to be controlled by a sim-server"""

    def __init__(self, simulation: RunnableSimulation) -> None:

        self.simulation = simulation

        self.sim_process: Optional[Process] = None
        self.shared_state: dict = Manager().dict()
        self.should_run = Value(c_bool, False)
        self.factor: SyncedFloat = SyncedFloat._create_factor_instance()

    def start_simulation_process(self):
        self.reset_sim()
        self._setup_sim()
        self.sim_process.start()
        return "simulation process started"

    def _setup_sim(self):
        self.shared_state = Manager().dict()
        self.should_run.value = True
        self.sim_process = Process(
            target=self.simulation.simulate,
            args=(
                self.shared_state,
                self.should_run,
                self.factor,
            ),
        )

    def pause_sim(self):
        self.should_run.value = False
        return "paused"

    def resume_sim(self):
        self.should_run.value = True
        return "resumed"

    def reset_sim(self):
        if self.sim_process is not None and self.sim_process.is_alive():
            self.sim_process.terminate()
            self.sim_process = None
        self.should_run.value = False
        return "reset"

    def get_state_dumps(self):
        state = self._get_state_dumps()
        return json.dumps(state)

    def get_partial_state_dumps(self):
        state = self._get_partial_state_dumps()
        return json.dumps(state)

    def get_state_dumps_fb(self):
        state = self._get_state_dumps()
        return flatbuffer_serializer.serialize(state)

    def get_partial_state_dumps_fb(self):
        state = self._get_partial_state_dumps()
        return flatbuffer_serializer.serialize(state)

    def _get_state_dumps(self):
        self.shared_state[web_canvas.UPDATED_KEY] = set()  # reset
        state = self.shared_state.copy()
        del state[web_canvas.UPDATED_KEY]
        return state

    def _get_partial_state_dumps(self):
        updated_set = set(self.shared_state[web_canvas.UPDATED_KEY])
        state = self.shared_state.copy()
        self.shared_state[web_canvas.UPDATED_KEY] = set()  # reset
        del state[web_canvas.UPDATED_KEY]
        for not_updated in state.keys() - updated_set:
            del state[not_updated]
        return state

    def set_rt_factor(self, value: float):
        return "set factor to " + str(self.factor.set_value(value))

    def get_sim_width(self) -> int:
        return self.simulation.width

    def get_sim_height(self) -> int:
        return self.simulation.height
