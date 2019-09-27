import gym
from gym import spaces
import numpy as np


class Connect4Env(gym.Env):
    """Connect4 game environment"""

    metadata = {'render.modes': ['human']}

    def __init__(self, board_shape=(6, 7)):
        super(Connect4Env, self).__init__()

        self.board_shape = board_shape

        self.observation_space = spaces.Box(low=-1, high=1, shape=board_shape)
        self.action_space = spaces.Discrete(board_shape[1])

        self.current_player = 1
        # self.board = np.zeros(self.board_shape)
        self.board = [[0 for col in range(self.board_shape[1])] for row in range(self.board_shape[0])]

    def step(self, action):
        reward = -1
        done = False

        # Check and perform action
        action_performed = False
        for index in list(reversed(range(self.board_shape[0]))):
            if self.board[index][action] == 0:
                self.board[index][action] = self.current_player
                action_performed = True
                break

        self.current_player *= -1

        if not action_performed:
            print("Invalid action! Column is full already")

        # Check board for completion (win condition or draw)
        moves_left = False
        for i in range(self.board_shape[0]):
            for j in range(self.board_shape[1]):
                if self.board[i][j] == 0:
                    moves_left = True
                    break
        if not moves_left:
            reward = -1
            done = True
        else:
            reward = -1
            done = False
            # Check win condition
            for i in range(self.board_shape[0]):
                for j in range(self.board_shape[1]-3):
                    value = sum(self.board[i][j:j+4])
                    if abs(value) == 4:
                        reward = 1
                        done = True
                        break
            # Transpose array
            reversed_board = [list(i) for i in zip(*self.board)]
            for i in range(self.board_shape[1]):
                for j in range(self.board_shape[0]-3):
                    value = sum(reversed_board[i][j:j+4])
                    if abs(value) == 4:
                        reward = 1
                        done = True
                        break
            # Test diagonal
            for i in range(self.board_shape[0]-3):
                for j in range(self.board_shape[1]-3):
                    value = 0
                    for k in range(4):
                        value += self.board[i+k][j+k]
                        if abs(value) == 4:
                            reward = 1
                            done = True
                            break
            for i in range(self.board_shape[1]-3):
                for j in range(self.board_shape[0]-3):
                    value = 0
                    for k in range(4):
                        value += reversed_board[i+k][j+k]
                        if abs(value) == 4:
                            reward = 1
                            done = True
                            break

        return self.board, reward, done, {}

    def reset(self):
        self.current_player = 1
        # self.board = np.zeros(self.board_shape)
        self.board = [[0 for col in range(self.board_shape[1])] for row in range(self.board_shape[0])]
        return self.board

    def render(self, mode='human', close=False):
        pass

    def close(self):
        pass

    def is_valid_action(self, action):
        for index in list(reversed(range(self.board_shape[0]))):
            if self.board[index][action] == 0:
                return True

        return False
