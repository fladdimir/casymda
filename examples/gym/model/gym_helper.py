"""helper classes"""

from simpy import Event


class RewardHolder:
    step_reward: float = 0
    accumulated_reward: float = 0

    def increase_step_reward(self, by: float):
        self.step_reward += by
        self.accumulated_reward += by

    def reset_step_reward(self):
        self.step_reward = 0

    def reset_accumulated_reward(self):
        self.accumulated_reward = 0


class ActionHolder:
    action_needed: Event  # will be succeeded somewhere when an action is needed, so that we can run until
    provided_action: Event  # to be succeeded to communicate back the action to whereever its needed
