class PlotPoint():
    def __init__(self, winnings, tier, bet, won, game_step):
        self.winnings = winnings
        self.tier = tier  # loss, small win, med win, large win, jackpot
        self.bet = bet
        self.won = won
        self.game_step = game_step

    @classmethod
    def beginning(cls):
        return cls(None, None, None, None, 0)
