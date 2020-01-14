import unittest
import playerclass
import plotpoint
from player_policies import policy1

player_verbosity = False


class PlayerClassTests(unittest.TestCase):

    def test_handle_betting_result(self):
        player = playerclass.Player(test_policy, verbose=player_verbosity)
        player.net_profit = 10
        player.current_enjoyment = 50
        player.win_streak = 1
        player.loss_streak = 0

        pp = plotpoint.PlotPoint(15, 3, 3, True, 5)  # winnings, tier, bet, won, game_step
        player.handle_betting_result(pp)

        expected_enjoyment = 50 + 1 * 20 - pow(1.05, 5)

        self.assertEqual(player.net_profit, 25)
        self.assertEqual(player.current_enjoyment, expected_enjoyment)
        self.assertEqual(player.win_streak, 2)
        self.assertEqual(player.loss_streak, 0)

    def test_stop_playing_when_threshold_crossed(self):
        player = playerclass.Player(policy1, verbose=player_verbosity)
        player.current_enjoyment = player.pi['THRESHOLD_ENJOYMENT'] - 1
        self.assertEqual(player.select_action(), 0)

    def test_profit_change_upon_placing_bet(self):
        player = playerclass.Player(policy1, verbose=player_verbosity)
        np = player.net_profit
        a = player.select_action()
        self.assertEqual(player.net_profit, np - a)


test_policy = {
    # ----- Enjoyment ----- #
    # General #
    'ENJOYMENT_DECAY_BASE': 1.05,
    'THRESHOLD_ENJOYMENT': 10,

    # tiers #
    'tiers': {
        'LOSS': -7,
        'SMALL_WIN': 10,
        'MED_WIN': 15,
        'LARGE_WIN': 20,
        'JACKPOT': 50
    },

    'BETTING_PROBABILITIES': [0.5, 0.3, 0.2],

    # Losing Streaks #
    'FRESH_LOSS_MULTIPLIER': 0.5,
    'THREE_LOSS_STREAK_MULTIPLIER': 1,
    'FIVE_LOSS_STREAK_MULTIPLIER': 1.5,
    'LARGE_LOSS_STREAK_MULTIPLIER': 1.7,

    # Winning Streaks #
    'FRESH_WIN_MULTIPLIER': 1,
    'THREE_WIN_MULTIPLIER': 1.2,
    'FIVE_WIN_MULTIPLIER': 1.5,
    'LARGE_WIN_STREAK_MULTIPLIER': 1,

    # Comeback #
    'COMEBACK_BASE': 1.2
}


if __name__ == '__main__':
    unittest.main()
