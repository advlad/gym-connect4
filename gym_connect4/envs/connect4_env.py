from abc import ABC, abstractmethod
from typing import Tuple

import gym
import numpy as np
from gym import spaces, logger


class Player(ABC):
    """ Class used for evaluating the game """

    def __init__(self, env, name='Player'):
        self.name = name
        self.env = env

    @abstractmethod
    def get_next_action(self, state: np.ndarray) -> int:
        pass

    def learn(self, state, action, reward, done) -> None:
        pass


class RandomPlayer(Player):
    def __init__(self, env, name='RandomPlayer'):
        super(RandomPlayer, self).__init__(env, name)

    def get_next_action(self, state: np.ndarray) -> int:
        for _ in range(100):
            action = np.random.randint(self.env.action_space.n)
            if self.env.is_valid_action(action):
                return action
        raise Exception('Unable to determine a valid move! Maybe invoke at the wrong time?')


class Connect4Env(gym.Env):
    """
    Description:
        Connect4 game environment

    Observation:
        Type: Discreet(6,7)

    Actions:
        Type: Discreet(7)
        Num     Action
        x       Column in which to insert next token (0-6)

    Reward:
        Reward is 0 for every step.
        If there are no other further steps possible, Reward is 0.5 and termination will occur
        If it's a win condition, Reward will be 1 and termination will occur
        If it is an invalid move, Reward will be -1 and termination will occur

    Starting State:
        All observations are assigned a value of 0

    Episode Termination:
        No more spaces left for pieces
        4 pieces are present in a line: horizontal, vertical or diagonally
        An attempt is made to place a piece in an invalid location
    """

    metadata = {'render.modes': ['human']}

    LOSS_REWARD = -1
    DEF_REWARD = 0
    DRAW_REWARD = 0.5
    WIN_REWARD = 1

    def __init__(self, board_shape=(6, 7)):
        super(Connect4Env, self).__init__()

        self.board_shape = board_shape

        self.observation_space = spaces.Box(low=-1, high=1, shape=board_shape, dtype=int)
        self.action_space = spaces.Discrete(board_shape[1])

        self.current_player = 1
        self.board = np.zeros(self.board_shape, dtype=int)

    # def next_player(self, currrent_player: int) -> int:
    #     return (currrent_player + 1) % 2
    #
    # def play(self, player1: Player, player2: Player) -> int:
    #     """
    #     :return: -1 if wins player1, 1 if wins player2, 0 if it's a draw
    #     """
    #     players = [player1, player2]
    #     # ToDo: implement game loop from app.py
    #     return 1

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, dict]:
        reward = self.DEF_REWARD
        done = False

        if not self.is_valid_action(action):
            print("Invalid action, column is already full")
            return self.board, self.LOSS_REWARD, True, {}

        # Check and perform action
        for index in list(reversed(range(self.board_shape[0]))):
            if self.board[index][action] == 0:
                self.board[index][action] = self.current_player
                break

        self.current_player *= -1

        # Check if board is completely filled
        if np.count_nonzero(self.board[0]) == self.board_shape[1]:
            reward = self.DRAW_REWARD
            done = True
        else:
            # Check win condition
            if self.is_win_state():
                done = True
                reward = self.WIN_REWARD

        return self.board, reward, done, {}

    def reset(self) -> np.ndarray:
        self.current_player = 1
        self.board = np.zeros(self.board_shape, dtype=int)
        return self.board

    def render(self, mode: str = 'human', close: bool = False) -> None:
        pass

    def close(self) -> None:
        pass

    def is_valid_action(self, action: int) -> bool:
        if self.board[0][action] == 0:
            return True

        return False

    def is_win_state(self) -> bool:
        # Test rows
        for i in range(self.board_shape[0]):
            for j in range(self.board_shape[1] - 3):
                value = sum(self.board[i][j:j + 4])
                if abs(value) == 4:
                    return True

        # Test columns on transpose array
        reversed_board = [list(i) for i in zip(*self.board)]
        for i in range(self.board_shape[1]):
            for j in range(self.board_shape[0] - 3):
                value = sum(reversed_board[i][j:j + 4])
                if abs(value) == 4:
                    return True

        # Test diagonal
        for i in range(self.board_shape[0] - 3):
            for j in range(self.board_shape[1] - 3):
                value = 0
                for k in range(4):
                    value += self.board[i + k][j + k]
                    if abs(value) == 4:
                        return True

        reversed_board = np.fliplr(self.board)
        # Test reverse diagonal
        for i in range(self.board_shape[0] - 3):
            for j in range(self.board_shape[1] - 3):
                value = 0
                for k in range(4):
                    value += reversed_board[i + k][j + k]
                    if abs(value) == 4:
                        return True

        return False
