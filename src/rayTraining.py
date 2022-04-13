import ray
from ray import tune
from ray.tune.registry import register_env
from ray.rllib.examples.custom_env import CustomModel, TorchCustomModel
from ray.rllib.models import ModelCatalog
from multiagentEnvironment import MARLTippingPointEnv

env = MARLTippingPointEnv(1000, 2)
env_name = "MARLTippingPointEnv"
register_env(env_name, lambda _: MARLTippingPointEnv(1000, 2))

obs_space = env.observation_space
act_space = env.action_space
num_agents = env.num_agents

# Create a policy mapping
def gen_policy():
    return (None, obs_space, act_space, {})


policy_graphs = {}
for i in range(num_agents):
    policy_graphs["agent-" + str(i)] = gen_policy()


def policy_mapping_fn(agent_id):
    return "agent-" + str(agent_id)


ModelCatalog.register_custom_model("my_model", CustomModel)

ray.init()
tune.run(
    "PPO",
    stop={"training_iteration": 1e5},
    config={
        # "num_gpus": 0,
        # "num_workers": 1,
        "env": env_name,
        "multiagent": {
            "policies": policy_graphs,
            "policy_mapping_fn": policy_mapping_fn,
        },
        "model": {"custom_model": "my_model", "conv_filters": None},
    },
)
