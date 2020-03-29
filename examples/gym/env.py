"""wraps simpy-env as gym-env
provides a step function which simulates time between decisions"""
import sys
from typing import Tuple
from gym.core import Env
from gym.spaces import Space, Discrete
from simpy import Event, Environment

from examples.gym.model.gym_example_model import Model
from examples.gym.model.gym_helper import ActionHolder, RewardHolder


NUMBER_OF_ACTIONS = 2
NUMBER_OF_FRUIT_TYPES = 2

FINISHED_ENTITIES_TO_BE_DONE = 100


class FruitSimEnv(Env):
    """wraps a simulation model to be used as a gym environment"""

    reward_range = (-float("inf"), float("inf"))
    action_space = Discrete(NUMBER_OF_ACTIONS)
    observation_space = Discrete(NUMBER_OF_FRUIT_TYPES)
    model: Model
    sim_env: Environment

    # interface methods: step, reset, render

    def step(self, action: object) -> Tuple[object, float, bool, dict]:
        """takes action and executes simulation until next action is needed"""

        self.reward_holder.reset_step_reward()

        # provide action via event, so that an unknown subscriber can yield it
        self.action_holder.provided_action.succeed(action)
        self.action_holder.action_needed = Event(self.sim_env)

        self.model.env.run(until=self.action_holder.action_needed)

        self.finished_gym_steps += 1

        observation: object = self.get_observation()
        reward: float = self.get_reward()
        done: bool = self.check_if_model_is_done()
        info: dict = {}

        return (observation, reward, done, info)

    def reset(self):
        """resets env and simulation model and return initial observation"""

        self.initialize_model()
        self.reward_holder.reset_accumulated_reward()
        self.reward_holder.reset_step_reward()

        self.action_holder.action_needed = Event(self.sim_env)
        self.model.env.run(until=self.action_holder.action_needed)

        initial_observation = self.get_observation()
        return initial_observation

    def render(self, mode=None):
        """animation is intended to be controlled via sim env visualizer"""
        pass

    # helper methods

    def get_observation(self):
        fruit = self.model.sorter.entities[0]
        fruit_types = ["apple", "pear"]
        index = fruit_types.index(fruit.fruit_type)
        return index

    def get_reward(self):
        return self.reward_holder.step_reward

    def check_if_model_is_done(self) -> bool:
        done = (
            self.model.apple_sink.overall_count_in
            + self.model.pear_sink.overall_count_in
            == FINISHED_ENTITIES_TO_BE_DONE
        )
        if done:
            print(self.reward_holder.accumulated_reward)
        return done

    def initialize_model(self):
        self.finished_gym_steps = 0

        self.sim_env = Environment()
        self.model = Model(self.sim_env)

        self.model.apple_source.max_entities = sys.maxsize
        self.model.pear_source.max_entities = sys.maxsize

        self.reward_holder = RewardHolder()
        self.model.apple_sink.reward_holder = self.reward_holder
        self.model.pear_sink.reward_holder = self.reward_holder

        self.action_holder = ActionHolder()
        self.model.sorter.action_holder = self.action_holder
