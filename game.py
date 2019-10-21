# generates results for each round using certain probaiblity
# this probability can be modified by the DM
# support for loading player and simulating
# TODO incorporate RTP (return to player) and betting amounts? player choose number of coins to bet?

import numpy as np

from plotpoint import PlotPoint
from constants import *


class LotteryGame():
    def __init__(self, dm, player, probabilities):
        self.game_step = 0
        self.dm = dm
        self.player = player
        self.available_actions = ['do nothing', 'increase win', 'big increase win', 'decrease win', 'big decrease win']  # TODO update avail actions?
        self.plot_point = PlotPoint.beginning()

        probabilities = np.array(probabilities)
        self.probabilities = probabilities  # loss, small, med, large, jackpot

        # set base probs -- used for in/decrementing winning probabilities. normalises all winning probs and make sure it sums to 1%
        self.base_probabilities = probabilities[1:] / probabilities[1:].sum()

    def step(self):
        print('Game\n\tstep: ' + str(self.game_step))

        # get action from DM
        dm_action = self.dm.get_action(self.available_actions, self.get_game_status(), self.player.get_status())
        self.run_dm_action(dm_action)

        # get action from player
        player_action = self.player.select_action(self.plot_point)

        if player_action == 0:
            done = True
        else:
            self.play_lottery(player_action)
            done = False

        return done

    def play_lottery(self, bet):
        self.game_step += 1
        tier = RESULTS[ np.random.choice(len(self.probabilities), p=self.probabilities) ]
        winnings = bet * WINNING_MULTIPLIER[tier]
        won = False if tier == 0 else True
        self.plot_point = PlotPoint(winnings, tier, bet, won, self.game_step)

    def run_dm_action(self, action):
        multiplier = 0
        if action == 'do nothing':
            return

        elif action == 'increase win':
            multiplier = SMALL_INC_WIN_PROB

        elif action == 'big increase win':
            multiplier = LARGE_INC_WIN_PROB

        elif action == 'decrease win':
            multiplier = SMALL_DEC_WIN_PROB

        elif action == 'big decrease win':
            multiplier = LARGE_DEC_WIN_PROB

        self.probabilities[1:] += multiplier * self.base_probabilities
        self.probabilities[0] -= multiplier

        for idx, value in enumerate(self.probabilities):
            if value <= 0:
                self.probabilities[idx] = MIN_PROBABILITY

        # rebalance probabilities to sum to 1.
        self.probabilities = self.probabilities / sum(self.probabilities)

    def get_game_status(self):
        return {'p': self.probabilities, 'plot_point': self.plot_point}
