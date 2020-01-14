from sarsa_dm import DM
import playerclass
import lotterygame
import player_policies
from statistics import mean, variance

dm = DM()

training_data = []
game_steps = []

for game_number in range(100):
    print(f'Game {game_number}')

    # FIXME implement reset function for player and game
    player = playerclass.Player(player_policies.policy1)
    game = lotterygame.LotteryGame(player)
    # FIXME change available actions to numbers instead of strings
        # this will probably break a few things
    prev_state = prev_action = None
    game_experience = []

    for i in range(100):
        if i == 0:
            # game just started
            prev_action = 'do nothing'

        new_state, reward, done = game.step(prev_action)  # gets DM action after passing in game + player status. runs action, then creates new state.

        new_action, new_q = dm.get_action(new_state)

        target_q = dm.get_q_value(reward, new_q)

        # TODO experience replay?
        if prev_state:
            experience_tuple = dm.get_experience_tuple(prev_state, prev_action, target_q)
            game_experience.append(experience_tuple)

        prev_state = new_state
        prev_action = new_action

        if done:
            # do something
            print('done')
            game_steps.append(i)
            break
        
        print('--')

    training_data += game_experience
    if len(training_data) > 40:
        dm.train_network(training_data)  # TODO rename this
        training_data = []

if len(training_data) > 0:
    dm.train_network(training_data)  # TODO rename this

print(f'Mean Steps: {mean(game_steps)}')
print(f'Variance: {variance(game_steps)}')
print(f'Max Steps: {max(game_steps)}')
print(f'Min Steps: {min(game_steps)}')
dm.plot_loss()
