import os
from marl_baselines3.independent_ppo import IndependentPPO
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.vec_env import DummyVecEnv
from multiagentEnvironment import MARLTippingPointEnv

# Logging
log_dir = "logs/"
os.makedirs(log_dir, exist_ok=True)

# Environment
num_agents = 2
timesteps = 1e4
env = MARLTippingPointEnv(1000, num_agents)
eval_callback = EvalCallback(DummyVecEnv([lambda: env]), best_model_save_path=log_dir,
			     log_path=log_dir, eval_freq=200,
			     deterministic=True, render=False)
# check_env(env)

# Policy network
model = IndependentPPO(
    "MultiInputPolicy",
    num_agents,
    env,
    verbose=2,
    tensorboard_log=log_dir + "/tensorboard",
)
model.learn(total_timesteps=int(timesteps), callbacks=[eval_callback] * num_agents)
