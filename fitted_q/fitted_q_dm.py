from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
# import pickle
# import pdb

FOREST_SAVE_DIRECTORY = '/forests/'


class FittedQDm():
    def __init__(self, params):
        self.gamma = params['GAMMA']
        self.prune = params['PRUNE']
        self.n_estimators = params['N_ESTIMATORS']
        self.n_min_values = params['N_MIN_VALUES']
        self.forests = None

    def create_forests(self, game_experience):
        # construct initial training set - just use rewards
        print('Building iteration 1')
        self.forests = {}
        for key, experience in game_experience.items():
            zipped = list(zip(*experience))
            prev_states = zipped[0]
            rewards = zipped[1]

            # regressor = ExtraTreesRegressor(n_estimators=self.n_estimators)
            # regressor.fit(prev_states, rewards)

            self.forests[key] = self.build_extra_trees_regressor(prev_states, rewards)
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

        return self.build_extra_trees_regressor(x, y)

    def build_extra_trees_regressor(self, x, y):
        chosen_n_min = 2  # default value, whether pruned or not

        # do pruning here
        if self.prune:
            # As detailed in the fitted q paper, we take a cross-validation approach to
            # select the best n_min to prune the forests with.
            x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.66)

            best_mse = None

            for n_min in self.n_min_values:
                reg = ExtraTreesRegressor(n_estimators=self.n_estimators, min_samples_split=n_min)
                reg.fit(x_train, y_train)
                y_pred = reg.predict(x_test)
                mse_value = mean_squared_error(y_pred, y_test)
                if not best_mse or mse_value < best_mse:
                    best_mse = mse_value
                    chosen_n_min = n_min
            # print(f'Chosen n_min for pruning: {chosen_n_min}')

        regressor = ExtraTreesRegressor(n_estimators=self.n_estimators, min_samples_split=chosen_n_min)
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

    def save_forest(self):
        path_to_file = FOREST_SAVE_DIRECTORY + 'iteration_' + str(self.num_iterations)
        
    # def plot_loss(self):
    #     # plot loss history
    #     plt.plot(self.loss_history)
    #     plt.show()
