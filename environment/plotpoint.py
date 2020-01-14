from .constants import LOTTERY_RESULTS


class PlotPoint():
    def __init__(self, winnings, tier_idx, bet, won, game_step):
        self.winnings = winnings
        self.tier = LOTTERY_RESULTS[tier_idx]  # loss, small win, med win, large win, jackpot
        self.bet = bet
        self.won = won
        self.game_step = game_step

    @classmethod
    def beginning(cls):
        return cls(None, 0, None, None, 0)
