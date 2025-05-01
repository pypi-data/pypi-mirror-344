from rnl.configs.config import (
    EnvConfig,
    RenderConfig,
    RobotConfig,
    SensorConfig,
)
from rnl.configs.rewards import RewardConfig
from rnl.engine.utils import _parse_simple_yaml
import torch
import os
from agilerl.hpo.mutation import Mutations
from agilerl.hpo.tournament import TournamentSelection

from agilerl.training.train_on_policy import train_on_policy
from agilerl.utils.utils import (
   create_population,
   observation_space_channels_to_first
)
from rnl.engine.vector import make_vect_envs_norm

def main():
    configs = _parse_simple_yaml("rnl/configs/train_configs.yaml")

    robot_config = RobotConfig(
        base_radius=configs["robot"]["base_radius"],
        vel_linear=[configs["robot"]["vel_linear"][0], configs["robot"]["vel_linear"][1]],
        vel_angular=[configs["robot"]["vel_angular"][0], configs["robot"]["vel_angular"][1]],
        wheel_distance=configs["robot"]["wheel_distance"],
        weight=configs["robot"]["weight"],
        threshold=configs["robot"]["threshold"],
        collision=configs["robot"]["collision"],
        noise=False,
        path_model="None",
    )
    sensor_config = SensorConfig(
        fov=configs["sensor"]["fov"],
        num_rays=configs["sensor"]["num_rays"],
        min_range=configs["sensor"]["min_range"],
        max_range=configs["sensor"]["max_range"]
    )
    env_config = EnvConfig(
        scalar=configs["env"]["scalar"],
        folder_map=configs["env"]["folder_map"],
        name_map=configs["env"]["name_map"],
        timestep=configs["env"]["timestep"],
        obstacle_percentage=configs["env"]["obstacle_percentage"],
        map_size=configs["env"]["map_size"],
        type=configs["env"]["type"],
        grid_size=configs["env"]["grid_size"]
    )
    render_config = RenderConfig(
        controller=configs["render"]["controller"],
        debug=configs["render"]["debug"],
        plot=configs["render"]["plot"]
    )

    reward_config = RewardConfig(
        params={
            "scale_orientation": 0.0,
            "scale_distance": 0.0,
            "scale_time": 0.01,
            "scale_obstacle": 0.0,
        },
    )

    config = {
        "robot_config": robot_config,
        "sensor_config": sensor_config,
        "env_config": env_config,
        "render_config": render_config,
        "reward_config": reward_config,
    }

    print(config)

    NET_CONFIG = {
    "encoder_config": {"hidden_size": [64, 64]}
    }

    INIT_HP = {
    "ENV_NAME": "NaviEnv",
    "ALGO": "PPO",
    "POPULATION_SIZE": 2,
    "BATCH_SIZE": configs["trainer"]["batch_size"],
    "LR": configs["trainer"]["lr"],
    "LEARN_STEP": configs["trainer"]["learn_step"],
    "GAMMA": 0.99,
    "GAE_LAMBDA": configs["trainer"]["gae_lambda"],
    "ACTION_STD_INIT": 0.6,
    "CLIP_COEF": 0.2,
    "ENT_COEF": configs["trainer"]["ent_coef"],
    "VF_COEF": configs["trainer"]["vf_coef"],
    "MAX_GRAD_NORM": configs["trainer"]["max_grad_norm"],
    "TARGET_KL": None,
    "TARGET_SCORE": 1,
    "MAX_STEPS": int(configs["trainer"]["max_timestep_global"]),
    "EVO_STEPS": 100,
    "UPDATE_EPOCHS": configs["trainer"]["update_epochs"],
    "CHANNELS_LAST": False,
    "WANDB": False,
    }

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Directory to save trained agents and skills
    save_dir = "./models/agilerl"
    os.makedirs(save_dir, exist_ok=True)

    num_envs = 12
    env = make_vect_envs_norm(
        num_envs=num_envs,
        robot_config=robot_config,
        sensor_config=sensor_config,
        env_config=env_config,
        render_config=render_config,
        use_render=False,
        type_reward=reward_config,
    )

    observation_space = env.single_observation_space
    action_space = env.single_action_space
    pop = create_population(
            algo="PPO",  # Algorithm
            observation_space=observation_space,  # Observation space
            action_space=action_space,  # Action space
            net_config=NET_CONFIG,  # Network configuration
            INIT_HP=INIT_HP,  # Initial hyperparameters
            population_size=INIT_HP["POPULATION_SIZE"],  # Population size
            device=device,
    )

    tournament = TournamentSelection(
        tournament_size=2,  # Tournament selection size
        elitism=True,  # Elitism in tournament selection
        population_size=INIT_HP["POPULATION_SIZE"],  # Population size
        eval_loop=1,  # Evaluate using last N fitness scores
    )

    mutations = Mutations(
        no_mutation=0.2,  # No mutation
        architecture=0.4,  # Architecture mutation
        new_layer_prob=0.4,  # New layer mutation
        parameters=0.4,  # Network parameters mutation
        activation=0.2,  # Activation layer mutation
        rl_hp=0.2,  # Learning HP mutation
        mutation_sd=0.1,  # Mutation strength  # Network architecture
        rand_seed=1,  # Random seed
        device=device,
    )

    trained_pop, pop_fitnesses = train_on_policy(
            env=env,  # Gym-style environment
            env_name=f"{INIT_HP['ENV_NAME']}",  # Environment name
            algo=INIT_HP["ALGO"],  # Algorithm
            pop=pop,  # Population of agents
            swap_channels=INIT_HP[
                "CHANNELS_LAST"
            ],
            max_steps=INIT_HP["MAX_STEPS"],  # Max number of training episodes
            evo_steps=INIT_HP["EVO_STEPS"],  # Evolution frequency
            target=INIT_HP["TARGET_SCORE"],  # Target score for early stopping
            tournament=tournament,  # Tournament selection object
            mutation=mutations,  # Mutations object
            wb=INIT_HP["WANDB"],  # Weights and Biases tracking
            checkpoint=configs["trainer"]["checkpoint"],
            checkpoint_path=configs["trainer"]["checkpoint_path"]
    )

    # Save the trained algorithm
    # filename = "PPO_trained_agent_param.pt"
    # save_path = os.path.join(save_dir, filename)
    # trained_pop[0].save_checkpoint(save_path)

    print(trained_pop[0])

    env.close()


if __name__ == "__main__":
    main()
