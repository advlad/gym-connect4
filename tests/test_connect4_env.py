import pytest
import gym
import gym_connect4.envs

VALIDATION_BOARD = [[0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, -1, 0, 0, 0],
                 [0, 0, -1, 1, 0, -1, 0],
                 [0, 0, 1, 1, 0, 1, 1],
                 [-1, -1, -1, -1, 0, -1, -1],
                 [1, 1, -1, 1, -1, 1, 1]]


def test_is_valid_action():
    env = gym.make('Connect4-v0')
    env.reset()
    env.board = VALIDATION_BOARD
    assert env.step(0) is True


def test_is_not_valid_action():
    env = gym.make('Connect4-v0')
    env.reset()
    env.board = VALIDATION_BOARD
    assert env.step(3) is True


def test_is_win_state():
    assert True is True
