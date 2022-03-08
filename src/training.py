import gym
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import PPO

from environment import TippingPointEnv

env = DummyVecEnv([lambda: TippingPointEnv(301)])
model = PPO("MlpPolicy", env)
model.learn(total_timesteps=300)

obs = env.reset()
for i in range(300):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
