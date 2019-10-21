import numpy as np


class DM():
    def __init__(self):
        pass

    def get_action(self, available_actions, game_status, player_status):
        # game status: (winning probabilities, plot point)
        # player status: (net profit, current enjoyment, win streak, loss streak, policy)
        print('DM')
        if game_status['plot_point'].game_step == 0:
            return 'do nothing'

        # random action
        action = np.random.choice(available_actions)
        print('\taction: ' + action)
        return action
