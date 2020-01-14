import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data
import matplotlib.pyplot as plt


class DM():
    def __init__(self):
        # FIXME intialiser should take in these variables
        # FIXME or place these in a constants file
        self.e_greedy_threshold = 0.2
        self.network = SarsaNet()
        self.gamma = 0.3
        self.lr = 0.01
        self.batch_size = 16
        self.epochs = 3

        self.loss_history = []

    def get_action(self, state):
        # game status: (winning probabilities, plot point)
        # player status: (net profit, current enjoyment, win streak, loss streak)
        available_actions, game_status, player_status = state
        print('DM')
        if game_status['plot_point'].game_step == 0:
            return 'do nothing'

        nn_input = self.parse_status(available_actions, game_status, player_status)

        res = self.network(nn_input).detach().numpy()
        # epsilon greedy
        if random.random() > self.e_greedy_threshold:
            # perform greedy action
            idx = np.argmax(res)
        
        else:
            # random action
            idx = np.random.choice(available_actions)

        action = available_actions[idx]
        q = res[idx]

        print('\taction: ' + action)
        return action, q

    def parse_status(self, available_actions, game_status, player_status):
        '''
        game_status: {
            p: probabilities -> (1x5 vector)
            plot_point: plot point -> (winnings, tier, bet, won, game_step) this will be the lottery result from the previous player action
        }

        player_status: net_profit, current_enjoyment, win_streak, loss_streak
        '''
        nn_input = []

        nn_input_row = game_status['p'].tolist()
        nn_input_row += [ game_status['plot_point'].game_step ]
        nn_input_row += [ player_status[0] ]
        nn_input_row += list(player_status[2:])

        for i in available_actions:
            nn_input.append(nn_input_row + [i])

        nn_input = torch.Tensor(nn_input).float()
        
        return nn_input

    def get_experience_tuple(self, state, action, target_q):
        available_actions, game_status, player_status = state

        nn_input_vector = self.parse_status(available_actions, game_status, player_status)
        # idx = available_actions.index(action)
        # nn_input = nn_input_vector[idx]
        nn_input = nn_input_vector[action]

        return (nn_input, target_q)

    def get_q_value(self, reward, new_q):
        return reward + self.gamma * new_q

    def train_network(self, training_data):
        # split into mini batches
        # train for multiple epochs?
        optimizer = optim.Adam(self.network.parameters(), lr=self.lr)
        criterion = nn.MSELoss()
        dataloader = torch.utils.data.DataLoader(training_data, batch_size=self.batch_size)
        for e in range(self.epochs):
            print(f'training epoch {e}')
            for idx, (x, y) in enumerate(dataloader):
                x = torch.autograd.Variable(x).float()
                y = torch.autograd.Variable(y).float()
                optimizer.zero_grad()
                y_hat = self.network(x)
                loss = criterion(y_hat, y)
                loss.backward()
                optimizer.step()
                self.loss_history.append(loss.item())

    def plot_loss(self):
        # plot loss history
        plt.plot(self.loss_history)
        plt.show()


class SarsaNet(nn.Module):

    def __init__(self):
        super(SarsaNet, self).__init__()
        self.fc1 = nn.Linear(10, 20)
        self.fc2 = nn.Linear(20, 50)
        self.fc3 = nn.Linear(50, 30)
        self.output = nn.Linear(30, 1)

        self.leaky_relu = nn.LeakyReLU(0.1)

    def forward(self, x):
        x = self.leaky_relu(self.fc1(x))
        x = self.leaky_relu(self.fc2(x))
        x = self.leaky_relu(self.fc3(x))
        x = self.output(x)
        return x
