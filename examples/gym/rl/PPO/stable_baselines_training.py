from examples.gym.env import FruitSimEnv

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

STEPS = 10000
SAVE_NAME = "_temp_PPO2_fruit_env_" + str(STEPS)


def stable_baselines_training():

    env = FruitSimEnv()
    env = DummyVecEnv(
        [lambda: env]
    )  # The algorithms require a vectorized environment to run

    model = PPO2(MlpPolicy, env, verbose=0)
    model.learn(total_timesteps=STEPS)

    model.save(SAVE_NAME)

    del model  # remove to demonstrate saving and loading

    model = PPO2.load(SAVE_NAME)

    obs = env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        env.render()

    print("done")
