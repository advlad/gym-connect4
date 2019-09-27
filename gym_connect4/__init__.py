from gym.envs.registration import register
from .envs.connect4_env import Connect4Env, Player, RandomPlayer

register(
    id='Connect4-v0',
    entry_point='gym_connect4.envs:Connect4Env',
)
