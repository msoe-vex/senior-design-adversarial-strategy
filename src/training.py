import os
import gym
import matplotlib.pyplot as plt
from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv
from stable_baselines3.common.vec_env.vec_transpose import VecTransposeImage
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from environment import TippingPointEnv

# Logging
log_dir = "logs/"
os.makedirs(log_dir, exist_ok=True)

# Environment
env = TippingPointEnv(1000)
# check_env(env)
env = Monitor(env)
env = DummyVecEnv([lambda: env])
# env = VecTransposeImage(env)

# Policy network
timesteps = 1e4
model = PPO(
    "MultiInputPolicy", env, verbose=2, tensorboard_log=log_dir + "/tensorboard"
)
model.learn(total_timesteps=int(timesteps))

# Rendering example:
# obs = env.reset()
# for i in range(100):
#     action, _states = model.predict(obs)
#     action = env.action_space.sample()
#     obs, rewards, done, info = env.step(action)
#     env.render()

# plt.show()
