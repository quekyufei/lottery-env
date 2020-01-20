class HardCodeDm():
    def __init__(self, params):
        self.focus = params['FOCUS']

    def get_action(self, state):
        if self.focus == 'game_length':
            return self.get_game_length_action(state)
        elif self.focus == 'casino_profits':
            return self.get_casino_profits_action(state)

    def get_game_length_action(self, state):
        # actions: 'do nothing', 'increase win', 'big increase win', 'decrease win', 'big decrease win'
        available_actions, game_status, player_status = state
        profit, _, win_streak, loss_streak = player_status
        
        if win_streak > 0 and win_streak < 3:
            return 3  # decrease win
        elif win_streak >= 3 and win_streak < 5:
            return 0
        elif win_streak >= 5:
            return 4
        elif loss_streak > 0 and loss_streak < 3:
            return 1
        elif loss_streak >= 3 and loss_streak < 5:
            return 0
        elif loss_streak >= 5:
            return 2
        else:
            return 0

    def get_casino_profits_action(self, state):
        available_actions, game_status, player_status = state
        player_profit, _, _, _ = player_status
        casino_profits = -player_profit
        
        if casino_profits < -50:
            return 4
        elif casino_profits < 0:
            return 3
        elif casino_profits > 5:
            return 1
        elif casino_profits > 10:
            return 2
        else:
            return 0
