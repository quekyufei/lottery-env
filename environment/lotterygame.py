# generates results for each round using certain probaiblity
# this probability can be modified by the DM
# support for loading player and simulating
# TODO incorporate RTP (return to player) and betting amounts? player choose number of coins to bet?

import numpy as np

from .plotpoint import PlotPoint
from .constants import *


class LotteryGame():
    def __init__(self, player, verbose=True):
        self.verbose = verbose
        self.game_step = 0
        self.player = player
        self.available_actions = [0, 1, 2, 3, 4]  # 'do nothing', 'increase win', 'big increase win', 'decrease win', 'big decrease win'
        self.plot_point = PlotPoint.beginning()
        self.initialise_probabilities(RELATIVE_WINNING_RATIOS, WIN_CHANCE)

    def step(self, dm_action):
        self.game_step += 1
        if self.verbose: print('Game\n\tstep: ' + str(self.game_step))

        reward = self.calculate_next_state(dm_action)

        # get action from player (this is part of calculating next state for DM)
        player_action = self.player.select_action()

        if player_action == 0:
            done = True
        else:
            self.play_lottery(player_action)
            done = False

        self.player.handle_betting_result(self.plot_point)

        return (self.available_actions, self.get_game_status(), self.player.get_status()), reward, done

    def calculate_next_state(self, dm_action):
        self.run_dm_action(dm_action)
        return self.get_reward()

    def run_dm_action(self, action):
        # Modify lottery probabilities according to DM actions.
        if action == 0:  # 'do nothing'
            return

        multiplier = PROBABILITY_MODIFIER_MULTIPLIER[action]

        self.lottery_probs[1:] += multiplier * np.array(self.relative_winning_percentage)
        self.lottery_probs[0] -= multiplier

        for idx, value in enumerate(self.lottery_probs):
            if value <= 0:
                self.lottery_probs[idx] = MIN_PROBABILITY

        # rebalance probabilities to sum to 1, as setting to min prob might have caused sum != 1
        self.lottery_probs = self.lottery_probs / sum(self.lottery_probs)

    def get_reward(self):
        '''
        # Player enjoyment reward function
        # simple reward to encourage maximising happiness: current enjoyment - threshold enjoyment
        # TODO why bother with threshold? why not use 0?

        current_enjoyment = self.player.current_enjoyment
        threshold_enjoyment = self.player.pi['THRESHOLD_ENJOYMENT']
        return current_enjoyment - threshold_enjoyment
        '''

        # net casino profits as reward function
        # casino profits == negative of player profits
        return -self.player.net_profit

    def play_lottery(self, bet):
        tier = np.random.choice(self.available_actions, p=self.lottery_probs)
        winnings = bet * WINNING_MULTIPLIER[tier]
        won = False if tier == 0 else True
        self.plot_point = PlotPoint(winnings, tier, bet, won, self.game_step)

    def reset(self):
        self.game_step = 0
        self.player.reset()
        self.plot_point = PlotPoint.beginning()
        self.initialise_probabilities(RELATIVE_WINNING_RATIOS, WIN_CHANCE)

    def get_game_status(self):
        return {'p': self.lottery_probs, 'plot_point': self.plot_point}

    def get_weighted_random_action(self):
        return np.random.choice(self.available_actions, size=1, p=WEIGHTED_ACTION_PROBS).item()

    def initialise_probabilities(self, relative_winning_ratios, win_chance):
        # sets probabilities with values from constants.py
        self.relative_winning_percentage = relative_winning_ratios / sum(relative_winning_ratios)
        self.lottery_probs = np.concatenate(([1 - win_chance], win_chance * self.relative_winning_percentage))

