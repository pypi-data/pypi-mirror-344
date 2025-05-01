from rnl.configs.config import (
    EnvConfig,
    NetworkConfig,
    RenderConfig,
    RobotConfig,
    SensorConfig,
    TrainerConfig,
)
from rnl.environment.env import NaviEnv
from rnl.configs.rewards import RewardConfig
from rnl.engine.utils import _parse_simple_yaml
import torch
import os
import numpy as np
import torch
import wandb
from tqdm import trange

from agilerl.algorithms.ppo import PPO
from agilerl.training.train_on_policy import train_on_policy
from agilerl.wrappers.learning import Skill
from agilerl.utils.algo_utils import obs_channels_to_first
from agilerl.utils.utils import (
   create_population,
   make_vect_envs,
   observation_space_channels_to_first
)
from rnl.training.utils import make_skill_vect_envs

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
    env_config_turn = EnvConfig(
        scalar=configs["env"]["scalar"],
        folder_map=configs["env"]["folder_map"],
        name_map=configs["env"]["name_map"],
        timestep=configs["env"]["timestep"],
        obstacle_percentage=configs["env"]["obstacle_percentage"],
        map_size=configs["env"]["map_size"],
        type="turn",
        grid_size=configs["env"]["grid_size"]
    )

    env_config_avoid = EnvConfig(
        scalar=configs["env"]["scalar"],
        folder_map=configs["env"]["folder_map"],
        name_map=configs["env"]["name_map"],
        timestep=configs["env"]["timestep"],
        obstacle_percentage=configs["env"]["obstacle_percentage"],
        map_size=configs["env"]["map_size"],
        type="avoid",
        grid_size=configs["env"]["grid_size"]
    )
    render_config = RenderConfig(
        controller=configs["render"]["controller"],
        debug=configs["render"]["debug"],
        plot=configs["render"]["plot"]
    )

    trainer_config = TrainerConfig(
        pretrained=configs["trainer"]["pretrained"],
        use_agents=configs["trainer"]["use_agents"],
        max_timestep_global=configs["trainer"]["max_timestep_global"],
        seed=configs["trainer"]["seed"],
        batch_size=configs["trainer"]["batch_size"],
        num_envs=configs["trainer"]["num_envs"],
        device=configs["trainer"]["device"],
        checkpoint=configs["trainer"]["checkpoint"],
        checkpoint_path=configs["trainer"]["checkpoint_path"],
        use_wandb=configs["trainer"]["use_wandb"],
        wandb_api_key=str(os.environ.get("WANDB_API_KEY")),
        wandb_mode="offline",
        llm_api_key=str(os.environ.get("GEMINI_API_KEY")),
        lr=configs["trainer"]["lr"],
        learn_step=configs["trainer"]["learn_step"],
        gae_lambda=configs["trainer"]["gae_lambda"],
        ent_coef=configs["trainer"]["ent_coef"],
        vf_coef=configs["trainer"]["vf_coef"],
        max_grad_norm=configs["trainer"]["max_grad_norm"],
        update_epochs=configs["trainer"]["update_epochs"],
        name=configs["trainer"]["name"],
        verbose=configs["trainer"]["verbose"],
        policy_type=configs["trainer"]["policy_type"],
    )

    network_config = NetworkConfig(
        hidden_size=configs["network"]["hidden_size"],
        mlp_activation=configs["network"]["mlp_activation"],
        type_model=configs["network"]["type_model"],
    )

    reward_config_turn = RewardConfig(
        params={
            "scale_orientation": 0.0,
            "scale_distance": 0.0,
            "scale_time": 0.01,
            "scale_obstacle": 0.0,
        },
    )

    reward_config_avoid = RewardConfig(
        params={
            "scale_orientation": 0.0,
            "scale_distance": 0.0,
            "scale_time": 0.01,
            "scale_obstacle": 0.004,
        },
    )


    config_turn = {
        "robot_config": robot_config,
        "sensor_config": sensor_config,
        "env_config": env_config_turn,
        "render_config": render_config,
        "trainer_config": trainer_config,
        "network_config": network_config,
        "reward_config": reward_config_turn,
    }

    config_avoid = {
        "robot_config": robot_config,
        "sensor_config": sensor_config,
        "env_config": env_config_avoid,
        "render_config": render_config,
        "trainer_config": trainer_config,
        "network_config": network_config,
        "reward_config": reward_config_avoid,
    }


    NET_CONFIG = {
    "encoder_config": {"hidden_size": [64, 64]}  # Actor encoder hidden size
    }

    INIT_HP = {
    "ENV_NAME": "NaviEnv",
    "ALGO": "PPO",
    "POPULATION_SIZE": 1,  # Population size
    "BATCH_SIZE": 128,  # Batch size
    "LR": 1e-3,  # Learning rate
    "LEARN_STEP": 128,  # Learning frequency
    "GAMMA": 0.99,  # Discount factor
    "GAE_LAMBDA": 0.95,  # Lambda for general advantage estimation
    "ACTION_STD_INIT": 0.6,  # Initial action standard deviation
    "CLIP_COEF": 0.2,  # Surrogate clipping coefficient
    "ENT_COEF": 0.01,  # Entropy coefficient
    "VF_COEF": 0.5,  # Value function coefficient
    "MAX_GRAD_NORM": 0.5,  # Maximum norm for gradient clipping
    "TARGET_KL": None,  # Target KL divergence threshold
    "TARGET_SCORE": 2000,
    "MAX_STEPS": 1_000_000,
    "EVO_STEPS": 10_000,
    "UPDATE_EPOCHS": 4,  # Number of policy update epochs
    "CHANNELS_LAST": False,
    "WANDB": True,
    }

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Directory to save trained agents and skills
    save_dir = "./models/PPO"
    os.makedirs(save_dir, exist_ok=True)


    env_turn = NaviEnv(
        robot_config,
        sensor_config,
        env_config_turn,
        render_config,
        use_render=False,
        mode=env_config_turn.type,
        type_reward=reward_config_turn,
    )

    env_avoid = NaviEnv(
        robot_config,
        sensor_config,
        env_config_avoid,
        render_config,
        use_render=False,
        mode=env_config_avoid.type,
        type_reward=reward_config_avoid,
    )

    skills = {
        "avoid": "avoid",
        "turn": "turn",
    }


    for skill_name in skills.keys():
        env = make_skill_vect_envs(
            INIT_HP["ENV_NAME"],
            env_turn,
            env_avoid,
            skill=skills[skill_name],
            num_envs=1
        )

        print(env)

        observation_space = env.single_observation_space
        action_space = env.single_action_space
        if INIT_HP["CHANNELS_LAST"]:
                observation_space = observation_space_channels_to_first(observation_space)

        pop = create_population(
                algo="PPO",  # Algorithm
                observation_space=observation_space,  # Observation space
                action_space=action_space,  # Action space
                net_config=NET_CONFIG,  # Network configuration
                INIT_HP=INIT_HP,  # Initial hyperparameters
                population_size=INIT_HP["POPULATION_SIZE"],  # Population size
                device=device,
        )

        trained_pop, pop_fitnesses = train_on_policy(
                env=env,  # Gym-style environment
                env_name=f"{INIT_HP['ENV_NAME']}-{skill_name}",  # Environment name
                algo=INIT_HP["ALGO"],  # Algorithm
                pop=pop,  # Population of agents
                swap_channels=INIT_HP[
                    "CHANNELS_LAST"
                ],  # Swap image channel from last to first
                max_steps=INIT_HP["MAX_STEPS"],  # Max number of training episodes
                evo_steps=INIT_HP["EVO_STEPS"],  # Evolution frequency
                target=INIT_HP["TARGET_SCORE"],  # Target score for early stopping
                tournament=None,  # Tournament selection object
                mutation=None,  # Mutations object
                wb=INIT_HP["WANDB"],  # Weights and Biases tracking
        )

        # Save the trained algorithm
        filename = f"PPO_trained_agent_{skill_name}.pt"
        save_path = os.path.join(save_dir, filename)
        trained_pop[0].save_checkpoint(save_path)

        env.close()


if __name__ == "__main__":
    main()
