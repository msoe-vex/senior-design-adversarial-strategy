import gym
import matplotlib.pyplot as plt
from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO

from environment import TippingPointEnv

env = TippingPointEnv(301)
check_env(env)
env = DummyVecEnv([lambda: env])
model = PPO("MlpPolicy", env)
model.learn(300)
# print(model.get_parameters())
total_reward = 0
obs = env.reset()
for i in range(100):
    action, _states = model.predict(obs)
    # action = env.action_space.sample()
    obs, rewards, done, info = env.step(action)
    # env.render()
    total_reward += rewards
print(total_reward / 100)
plt.show()
