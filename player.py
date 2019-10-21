# from constants import *
import numpy as np
import pdb


class Player():
    def __init__(self, starting_balance, policy):
        self.pi = policy
        self.starting_balance = starting_balance
        self.net_profit = 0
        self.history = []
        # current enjoyment will be determined by looking at the past 20 games. Losing streaks will decrease it, breaking a losing streak with a big win will greatly increase the enjoyment.
        self.current_enjoyment = 50
        self.loss_streak = 0
        self.win_streak = 0

    def select_action(self, plot_point):
        # TODO print out summary of state at each step
        print('Player')
        # pdb.set_trace()
        # if game just started, play
        if plot_point.bet is None:
            return np.random.choice([1, 2, 3], p=self.pi['BETTING_PROBABILITIES'])

        print('\tResult: ' + str(plot_point.tier))
        self.update_status(plot_point)
        # select to play or to leave
        if self.current_enjoyment < self.pi['THRESHOLD_ENJOYMENT']:
            # stop playing
            action = 0
        else:
            # choose whether to bet 1, 2, or 3 coins.
            action = np.random.choice([1, 2, 3], p=self.pi['BETTING_PROBABILITIES'])
            self.net_profit -= action

        print('\tEnjoyment: ' + str(round(self.current_enjoyment, 2)))
        print('\tCurrent Balance: ' + str(self.starting_balance + self.net_profit))
        print('\tAction: bet ' + str(action) + ' coins')
        return action

    def update_status(self, plot_point):
        self.history.append(plot_point)  # TODO can status include analysis on historical data like variance, mean?
        self.net_profit += plot_point.winnings
        enj_change = self.calculate_enjoyment_change(plot_point)
        self.current_enjoyment += enj_change
        self.current_enjoyment -= pow(self.pi['ENJOYMENT_DECAY_BASE'], plot_point.game_step)
        print('\tEnjoyment Change: ' + str(enj_change))
        print('\tEnjoyment Decay: ' + str(round(pow(self.pi['ENJOYMENT_DECAY_BASE'], plot_point.game_step), 2)))

        # update streaks
        if plot_point.won:
            self.win_streak += 1
            self.loss_streak = 0
        else:
            self.loss_streak += 1
            self.win_streak = 0

    def calculate_enjoyment_change(self, plot_point):
        enjoyment_change = 0
        tier_multiplier = self.pi['tiers'][plot_point.tier]
        if plot_point.won:
            # building win streak
            # comeback from loss streak
            if self.win_streak == 0:
                # was losing before this
                comeback_multiplier = pow(self.pi['COMEBACK_BASE'], self.loss_streak)
                enjoyment_change = self.pi['FRESH_WIN_MULTIPLIER'] * comeback_multiplier * tier_multiplier
                return enjoyment_change
            elif self.win_streak <= 2:
                enjoyment_change = self.pi['THREE_WIN_MULTIPLIER'] * tier_multiplier
                return enjoyment_change
            elif self.win_streak <= 4:
                enjoyment_change = self.pi['FIVE_WIN_MULTIPLIER'] * tier_multiplier
                return enjoyment_change
            elif self.win_streak > 4:
                enjoyment_change = self.pi['LARGE_WIN_STREAK_MULTIPLIER'] * tier_multiplier
                return enjoyment_change

        elif not plot_point.won:
            if self.loss_streak == 0:
                # previous was a win
                enjoyment_change = self.pi['FRESH_LOSS_MULTIPLIER'] * tier_multiplier
                return enjoyment_change
            elif self.loss_streak <= 2:
                # third loss in a row
                enjoyment_change = self.pi['THREE_LOSS_STREAK_MULTIPLIER'] * tier_multiplier
                return enjoyment_change
            elif self.loss_streak <= 4:
                enjoyment_change = self.pi['FIVE_LOSS_STREAK_MULTIPLIER'] * tier_multiplier
                return enjoyment_change
            elif self.loss_streak > 4:
                enjoyment_change = self.pi['LARGE_LOSS_STREAK_MULTIPLIER'] * tier_multiplier
                return enjoyment_change

    def get_status(self):
        # return status and policy
        return (self.net_profit, self.current_enjoyment, self.win_streak, self.loss_streak, self.pi)
