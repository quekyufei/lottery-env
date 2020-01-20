# General
VERBOSITY = False


# DM
DM_LIST = ['fittedq', 'sarsa', 'hardcoded']
DM_TYPE = DM_LIST[0]

LOTTERY_GAME_PARAMS = {
    'FOCUS': 'casino_profits',  # enjoyment or casino_profits
}


# --- Fitted Q Parameters -- #
FITTED_Q_PARAMS = {
    # General
    'NUM_INIT_GAMES': 300,  # number of games to play to gather initial data
    'NUM_TEST_GAMES': 300,  # number of games to run test on

    # Fitted Q Experiment
    'NUM_Q_FITTED_ITERATIONS': 25,  # number of fitted q iterations to fit

    # Fitted Q DM
    'GAMMA': 0.5,
    'PRUNE': True,
    'N_MIN_VALUES': [2, 3, 4, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    'N_ESTIMATORS': 50,
    
}

# --- SARSA NNet Parameters -- #
SARSA_NN_PARAMS = {
    # General
    'NUM_TRAINING_GAMES': 300,
}

# --- Hardcoded Parameters -- #
HARDCODED_PARAMS = {
    # General
    'NUM_GAMES': 300,

    # DM
    'FOCUS': 'game_length',  # game_length or casino_profits
}
