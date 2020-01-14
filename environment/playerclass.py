import numpy as np


class Player():
    def __init__(self, policy, verbose=True):
        self.verbose = verbose

        self.pi = policy
        self.net_profit = 0
        self.history = []
        self.current_enjoyment = 50
        self.loss_streak = 0
        self.win_streak = 0

    def reset(self):
        self.net_profit = 0
        self.history = []
        self.current_enjoyment = 50
        self.loss_streak = 0
        self.win_streak = 0

    def select_action(self):
        # select to play or to leave
        if self.current_enjoyment < self.pi['THRESHOLD_ENJOYMENT']:
            # stop playing
            action = 0
        else:
            # choose whether to bet 1, 2, or 3 coins.
            action = np.random.choice([1, 2, 3], p=self.pi['BETTING_PROBABILITIES'])
            self.net_profit -= action

        if self.verbose:
            print('Player')
            print(f'\tAction: bet {action} coins')
        
        return action

    def handle_betting_result(self, plot_point):
        self.history.append(plot_point)  # TODO can status include analysis on historical data like variance, mean?
        self.net_profit += plot_point.winnings
        enj_change = self.calculate_enjoyment_change(plot_point)
        enj_decay = pow(self.pi['ENJOYMENT_DECAY_BASE'], plot_point.game_step)
        self.current_enjoyment += enj_change
        self.current_enjoyment -= enj_decay

        # update streaks
        if plot_point.won:
            self.win_streak += 1
            self.loss_streak = 0
        else:
            self.loss_streak += 1
            self.win_streak = 0

        if self.verbose:
            print(f'\tBetting Result: {plot_point.tier}')
            print(f'\tPlayer\'s Net Profit: {self.net_profit}')
            print(f'\tEnjoyment Change: {enj_change}')
            print(f'\tEnjoyment Decay: {round(enj_decay, 2)}')
            print(f'\tCurrent Enjoyment: {round(self.current_enjoyment, 2)}')
            print(f'\tWin Streak: {self.win_streak}, Loss Streak: {self.loss_streak}')

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
            elif self.win_streak <= 1:
                enjoyment_change = self.pi['FRESH_WIN_MULTIPLIER'] * tier_multiplier
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
            if self.loss_streak <= 1:
                enjoyment_change = self.pi['FRESH_LOSS_MULTIPLIER'] * tier_multiplier
                return enjoyment_change
            elif self.loss_streak <= 2:
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
        return (self.net_profit, self.current_enjoyment, self.win_streak, self.loss_streak)
