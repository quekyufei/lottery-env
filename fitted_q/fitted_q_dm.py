from sklearn.ensemble import ExtraTreesRegressor
import numpy as np
# import pickle
# import pdb

FOREST_SAVE_DIRECTORY = '/forests/'


class FittedQDm():
    def __init__(self, gamma):
        self.gamma = gamma
        self.forests = None

    def create_forests(self, game_experience):
        # construct initial training set - just use rewards
        print('Building iteration 1')
        self.forests = {}
        for key, experience in game_experience.items():
            zipped = list(zip(*experience))
            prev_states = zipped[0]
            rewards = zipped[1]

            regressor = ExtraTreesRegressor(n_estimators=50)
            regressor.fit(prev_states, rewards)

            self.forests[key] = regressor
        self.num_iterations = 1

    def next_iteration(self, game_experience):
        print(f'Building iteration {self.num_iterations + 1}')
        new_forest = {}
        for key, experience in game_experience.items():
            new_forest[key] = self.update_forests(experience)

        self.forests = new_forest
        self.num_iterations += 1

    def update_forests(self, experience):
        x = []
        y = []

        for (prev_state, reward, next_state) in experience:
            max_reward = None
            for regressor in self.forests.values():
                if next_state:
                    # for last step in game, next state is None.
                    next_reward = regressor.predict([next_state])
                else:
                    # max_reward = np.array([reward - 30])  # 10 is arbitrary
                    max_reward = np.array([reward])  # when game ends, net casino profit has no change
                    break

                if not max_reward or (next_reward > max_reward):
                    max_reward = next_reward
            new_reward = reward + self.gamma * max_reward

            x.append(prev_state)
            y.append(new_reward.item())

        regressor = ExtraTreesRegressor(n_estimators=50)
        regressor.fit(x, y)
        return regressor

    def get_greedy_action(self, state):
        max_action = None
        max_reward = None
        state = [self.parse_state(state)]
        for action, regressor in self.forests.items():
            prediction = regressor.predict(state)
            if not max_reward or prediction > max_reward:
                max_reward = prediction.item()
                max_action = action

        return max_action

    def parse_status(self, num_actions, game_status, player_status):
        pass

    def get_experience_tuple(self, prev_state, reward, new_state):
        prev = self.parse_state(prev_state)
        new = self.parse_state(new_state)

        return (prev, reward, new)

    def parse_state(self, state):
        '''
        state (3-tuple): self.available_actions, self.get_game_status(), self.player.get_status()
            0. avail actions: 0, 1, 2, 3, 4
            1. game status: {'p': self.probabilities, 'plot_point': self.plot_point}
            2. player status: self.net_profit, self.current_enjoyment, self.win_streak, self.loss_streak
        '''

        available_actions, game_status, player_status = state

        tree_input = game_status['p'].tolist()
        tree_input += [ game_status['plot_point'].game_step ]
        tree_input += [ player_status[0] ]
        tree_input += list(player_status[2:])

        return tree_input

    def get_q_value(self, reward, new_q):
        pass

    def save_forest(self):
        path_to_file = FOREST_SAVE_DIRECTORY + 'iteration_' + str(self.num_iterations)
        
    # def plot_loss(self):
    #     # plot loss history
    #     plt.plot(self.loss_history)
    #     plt.show()
