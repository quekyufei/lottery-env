import os
import sys
import config
from environment import environment_loader

folderpath = os.getcwd()
sys.path.append(folderpath)

game = environment_loader.load_lottery_game(config.LOTTERY_GAME_PARAMS, config.VERBOSITY)

if config.DM_TYPE == 'fittedq':
    from fitted_q import fitted_q_experiment
    fitted_q_experiment.run(game, config.FITTED_Q_PARAMS)

elif config.DM_TYPE == 'sarsa':
    from sarsa import sarsa_experiment
    sarsa_experiment.run(game)

elif config.DM_TYPE == 'hardcoded':
    from hardcoded import hardcode_benchmark
    hardcode_benchmark.run(game, config.HARDCODED_PARAMS)
