from unittest import TestCase
from gym_connect4 import RandomPlayer

import gym

VALIDATION_BOARD = [[0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, -1, 0, 0, 0],
                 [0, 0, -1, 1, 0, -1, 0],
                 [0, 0, 1, 1, 0, 1, 1],
                 [-1, -1, -1, -1, 0, -1, -1],
                 [1, 1, -1, 1, -1, 1, 1]]


class TestConnect4Env(TestCase):

    def setUp(self) -> None:
        self.env = gym.make('Connect4-v0')


    def test_step(self):
        self.fail()

    def test_reset(self):
        self.fail()

    def test_is_valid_action(self):
        self.env = gym.make('Connect4-v0')
        self.env.reset()
        self.env.board = VALIDATION_BOARD
        self.assertTrue(self.env.is_valid_action(0))
        self.assertFalse(self.env.is_valid_action(3))

    def test_is_win_state(self):
        self.fail()
