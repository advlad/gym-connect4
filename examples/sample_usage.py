import gym
import gym_connect4
import numpy as np


env = gym.make('Connect4-v0')
env.reset()

total_reward = 0
done = False
while not done:

    for player in ['player1', 'player2']:
        while True:
            action = np.random.randint(env.action_space.n)
            if env.is_valid_action(action):
                break

        new_state, reward, done, _ = env.step(action)
        total_reward += reward
        if done:
            if reward == 1:
                print(f"winner: {player}")
                print("board state:\n", new_state)
                print(f"total reward={total_reward}")
            else:
                print("draw")
                print("board state:\n", new_state)
                print(f"total reward={total_reward}")
            break

env.close()
