from examples.gym.env import FruitSimEnv
from examples.gym.env import FINISHED_ENTITIES_TO_BE_DONE

from stable_baselines.common.env_checker import check_env


def test_stable_baselines_check():
    env = FruitSimEnv()
    check_env(env)


def test_fruit_env_fixed():

    env = FruitSimEnv()

    overall_reward = 0

    obs = env.reset()
    done = False
    while not done:
        action = 0
        obs, reward, done, info = env.step(action)
        overall_reward += reward

    assert env.finished_gym_steps == FINISHED_ENTITIES_TO_BE_DONE
    assert overall_reward == 0
    assert env.model.pear_sink.overall_count_in == FINISHED_ENTITIES_TO_BE_DONE


def test_fruit_env_correctly():

    env = FruitSimEnv()

    overall_reward = 0

    obs = env.reset()
    done = False
    while not done:
        # pears (obs: 1) should go up (0), apples down (1)
        action = 0 if obs == 1 else 1
        obs, reward, done, info = env.step(action)
        overall_reward += reward

    assert env.finished_gym_steps == FINISHED_ENTITIES_TO_BE_DONE
    assert overall_reward == FINISHED_ENTITIES_TO_BE_DONE
    assert env.model.pear_sink.overall_count_in == FINISHED_ENTITIES_TO_BE_DONE / 2
    assert env.model.apple_sink.overall_count_in == FINISHED_ENTITIES_TO_BE_DONE / 2
