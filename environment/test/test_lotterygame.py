import unittest
import lotterygame
from constants import *


class LotteryGameTests(unittest.TestCase):

    def test_initialise_probabilities(self):
        game = lotterygame.LotteryGame(player=None)
        game.initialise_probabilities(np.array([30, 15, 10, 5]), 0.60)
        self.assertTrue(np.allclose(game.lottery_probs, np.array([0.4, 0.3, 0.15, 0.1, 0.05])))

    def test_probability_modifier(self):
        game = lotterygame.LotteryGame(player=None)
        game.initialise_probabilities(np.array([30, 15, 10, 5]), 0.60)
        game.run_dm_action(1)
        self.assertTrue(np.allclose(game.lottery_probs, np.array([0.35, 0.325, 0.1625, 0.10833333, 0.05416667])))


if __name__ == '__main__':
    unittest.main()
