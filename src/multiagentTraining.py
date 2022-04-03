import os
from marl_baselines3.independent_ppo import IndependentPPO
from stable_baselines3.common.monitor import Monitor
from multiagentEnvironment import MARLTippingPointEnv

# Logging
log_dir = "logs/"
os.makedirs(log_dir, exist_ok=True)

# Environment
num_agents = 2
timesteps = 1e4
env = MARLTippingPointEnv(1000, num_agents)
# check_env(env)

# Policy network
model = IndependentPPO(
    "MultiInputPolicy",
    num_agents,
    env,
    verbose=2,
    tensorboard_log=log_dir + "/tensorboard",
)
model.learn(total_timesteps=int(timesteps))
