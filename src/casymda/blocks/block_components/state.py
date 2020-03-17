""" state management for blocks

a block is able to be in multiple states at a time

"""
from enum import Enum
from typing import Callable


class States(Enum):
    """ common block states """

    # this could be moved to owning class
    empty = "empty"  # "default", if all other states' count is 0
    busy = "busy"  # counted
    blocked = "blocked"  # by its successor, counted


class StateManager:
    """counts inc/dec events for each state and evaluates"""

    def __init__(self, on_state_change_callback: Callable[[States, bool], None]):
        self._counted_states = [States.busy, States.blocked]  # could be parameter
        self._default_state = States.empty  # could be parameter
        self._state_count = {state.value: 0 for state in self._counted_states}
        self._current_states = {state.value: False for state in States}
        self._on_state_change_callback = on_state_change_callback

    def increment_state_count(self, state):
        """increment_state_count"""
        self._change_state_count(state, 1)

    def decrement_state_count(self, state):
        """decrement_state_count"""
        self._change_state_count(state, -1)

    def _change_state_count(self, state, change):
        self._state_count[state.value] += change
        self.evaluate_state_count()

    def evaluate_state_count(self):
        """evaluate_state_count"""
        for state in self._counted_states:
            if self._state_count[state.value] > 0:
                self._set_new_state(state, True)
            else:
                self._set_new_state(state, False)

        if sum(self._state_count.values()) == 0:
            self._set_new_state(self._default_state, True)
        else:
            self._set_new_state(self._default_state, False)

    def _set_new_state(self, state, new_value):
        if self._current_states[state.value] != new_value:
            self._on_state_change_callback(state, new_value)
            self._current_states[state.value] = new_value
