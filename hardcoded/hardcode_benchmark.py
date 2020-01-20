from . import hardcode_dm
from statistics import mean


def run(game, params):
    print('# -- Hard Coded DM Benchmark -- #')
    print(f'Aiming to maximise {params["FOCUS"]}')
    num_games = params['NUM_GAMES']

    game_experience = {0: [], 1: [], 2: [], 3: [], 4: []}
    game_lengths = []
    game_profits = []
    dm = hardcode_dm.HardCodeDm(params)

    for game_num in range(num_games):
        game.reset()
        prev_action = 0  # do nothing
        
        for game_step in range(200):
            state, reward, done = game.step(prev_action)

            if done:
                game_lengths.append(game_step)
                game_profits.append(reward)
                break

            prev_action = dm.get_action(state)
            game_experience[prev_action].append('')

    print(f'All benchmark games done. Size of game experiences: 0: {len(game_experience[0])}, 1: {len(game_experience[1])}, 2: {len(game_experience[2])}, 3: {len(game_experience[3])}, 4: {len(game_experience[4])}')
    print(f'Average game length: {mean(game_lengths)}')
    print(f'Best game length: {max(game_lengths)}')
    print(f'Average casino profit: {mean(game_profits)}')
    print(f'Average casino profit: {max(game_profits)}')
    print('# -- Benchmarking Done -- #')
