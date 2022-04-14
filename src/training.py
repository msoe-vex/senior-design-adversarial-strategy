import os
import gym
import matplotlib.pyplot as plt
import io
import os
import cv2
import gym
import matplotlib
from matplotlib.transforms import Bbox
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv
from stable_baselines3.common.vec_env.vec_transpose import VecTransposeImage
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.monitor import Monitor
from environment import TippingPointEnv
from stable_baselines3.common.monitor import Monitor
from rl_training.environment import TippingPointEnv

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
timesteps = 1e5
checkpoint_callback = CheckpointCallback(
    save_freq=timesteps / 4, save_path=log_dir, name_prefix="strategyrl_model"
)
model = PPO(
    "MultiInputPolicy", env, verbose=2, tensorboard_log=log_dir + "/tensorboard"
)
model.learn(total_timesteps=int(timesteps), callback=checkpoint_callback)

matplotlib.use("Agg")
imgs = []
obs = env.reset()
fig = plt.figure()
canvas = FigureCanvas(fig)

for i in range(100):
    # action, _states = model.predict(obs)
    action = env.action_space.sample()
    obs, rewards, done, info = env.step(action)
    ax = env.render()

    # ax.axis("off")
    ax.figure.canvas.draw()
    # trans = ax.figure.dpi_scale_trans.inverted()
    # bbox = ax.bbox.transformed(trans)
    bbox = Bbox([[1.0, 1.0], [15, 10.75]])
    buff = io.BytesIO()
    plt.savefig(buff, format="jpg", dpi=ax.figure.dpi, bbox_inches=bbox, pad_inches=2)
    buff.seek(0)
    imgs.append(cv2.cvtColor(plt.imread(buff, "jpg"), cv2.COLOR_RGB2BGR))
    plt.close("all")

im_height, im_width, im_layers = imgs[0].shape
video = cv2.VideoWriter(
    "training.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (im_width, im_height)
)

for img in imgs:
    video.write(img)

video.release()
