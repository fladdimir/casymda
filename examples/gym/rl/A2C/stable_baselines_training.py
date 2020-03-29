from examples.gym.rl.PPO.stable_baselines_training import SAVE_NAME
from examples.gym.env import FruitSimEnv

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.vec_env import SubprocVecEnv
from stable_baselines import A2C

STEPS = 25000
SAVE_NAME = "_temp_A2C_fruit_env_" + str(STEPS)


def stable_baselines_training():

    # multiprocess environment
    n_cpu = 2
    env = FruitSimEnv()
    env = SubprocVecEnv([lambda: env for i in range(n_cpu)])

    model = A2C(MlpPolicy, env, verbose=1)
    model.learn(total_timesteps=STEPS)
    model.save(SAVE_NAME)

    del model  # remove to demonstrate saving and loading

    model = A2C.load(SAVE_NAME)

    sim_env = FruitSimEnv()
    env = DummyVecEnv([lambda: sim_env])

    obs = env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)

    print("done")
