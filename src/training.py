import os
import gym
import matplotlib.pyplot as plt
from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv
from stable_baselines3.common.vec_env.vec_transpose import VecTransposeImage
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.monitor import Monitor
from environment import TippingPointEnv

# Logging
log_dir = "logs/"
os.makedirs(log_dir, exist_ok=True)

# Environment
steps = 1000
env = TippingPointEnv(steps)
# check_env(env)
env = Monitor(env)
env = DummyVecEnv([lambda: env])
# env = VecTransposeImage(env)

# Policy network
timesteps = 1e4
checkpoint_callback = CheckpointCallback(
    save_freq=steps, save_path=log_dir, name_prefix="strategyrl_model"
)
model = PPO(
    "MultiInputPolicy", env, verbose=2, tensorboard_log=log_dir + "/tensorboard"
)
model.learn(total_timesteps=int(timesteps), callback=checkpoint_callback)

# Rendering example:
# obs = env.reset()
# for i in range(100):
#     action, _states = model.predict(obs)
#     action = env.action_space.sample()
#     obs, rewards, done, info = env.step(action)
#     env.render()

# plt.show()
