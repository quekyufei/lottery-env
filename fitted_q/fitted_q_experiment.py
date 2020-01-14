from . import fitted_q_dm
from statistics import mean
import numpy as np


def run(game, params):
    num_init_games = params['NUM_INIT_GAMES']
    num_fitted_q_iterations = params['NUM_Q_FITTED_ITERATIONS']
    num_test_games = params['NUM_TEST_GAMES']

    # gather experience with random replays
    print('# -- Generating Initial Games -- #')
    print(f'Number of games: {num_init_games}')
    # game experience split into the actions that were chosen
    game_experience = {0: [], 1: [], 2: [], 3: [], 4: []}
    init_game_lengths = []
    init_game_profits = []
    dm = fitted_q_dm.FittedQDm(params['GAMMA'])

    for game_num in range(num_init_games):
        game.reset()
        prev_state = None
        prev_action = 0  # do nothing
        
        for game_step in range(200):
            new_state, reward, done = game.step(prev_action)

            # save experience
            if prev_state and not done:  # on the first step of each game, prev_state is None.
                experience_tuple = dm.get_experience_tuple(prev_state, reward, new_state)
                game_experience[prev_action].append(experience_tuple)

            if done:
                experience_tuple = dm.get_experience_tuple(prev_state, reward, new_state)
                experience_tuple = (experience_tuple[0], experience_tuple[1], None)  # set "next state" to None
                game_experience[prev_action].append(experience_tuple)
                init_game_lengths.append(game_step)
                init_game_profits.append(reward)
                break

            prev_action = game.get_weighted_random_action()
            prev_state = new_state

    print(f'All initial games done. Size of game experiences: 0: {len(game_experience[0])}, 1: {len(game_experience[1])}, 2: {len(game_experience[2])}, 3: {len(game_experience[3])}, 4: {len(game_experience[4])}')
    print(f'Average game length: {mean(init_game_lengths)}')
    print(f'Average casino profit: {mean(init_game_profits)}')
    print('# -- Initial Games Generation Done -- #')

    iteration_average_game_length = []
    iteration_average_game_profits = []
    # train forest up to N iterations
    for n in range(num_fitted_q_iterations):
        if n == 0:
            dm.create_forests(game_experience)
        else:
            dm.next_iteration(game_experience)

        # -- TESTING -- #
        # use greedy action trained forests to run through games, gather average number of game steps (i.e. avg score)
        print(f'# -- Running Test Games For Iteration {n + 1} -- #')
        test_game_lengths = []
        test_game_profits = []
        test_chosen_actions = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        for game_num in range(num_test_games):
            game.reset()
            prev_action = 0  # do nothing
            
            for game_step in range(200):
                new_state, reward, done = game.step(prev_action)

                if done:
                    test_game_lengths.append(game_step)
                    test_game_profits.append(reward)
                    break

                prev_action = dm.get_greedy_action(new_state)
                test_chosen_actions[prev_action] += 1

        iteration_average_game_length.append(mean(test_game_lengths))
        iteration_average_game_profits.append(mean(test_game_profits))
        print(f'Iteration {n} test games done.')
        print(f'Average game length: {mean(test_game_lengths)}')
        print(f'Average game profits: {mean(test_game_profits)}')
        print(f'Actions Taken: {str(test_chosen_actions)}' )
        print('# -- Test Games Done -- #')

    print('# == All iterations done == #')
    print(f'Best average game length: {max(iteration_average_game_length)}')
    print(f'Best iteration for length: {np.argmax(iteration_average_game_length) + 1}')
    print(f'Length for each iteration: {iteration_average_game_length}')
    print(f'Best average profits: {max(iteration_average_game_profits)}')
    print(f'Best iteration for profits: {np.argmax(iteration_average_game_profits) + 1}')
    print(f'Length for each iteration: {iteration_average_game_profits}')


