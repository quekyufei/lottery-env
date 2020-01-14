# General
VERBOSITY = False


# DM
DM_LIST = ['fittedq', 'sarsa']
DM_TYPE = DM_LIST[0]


# --- Fitted Q Parameters -- #
FITTED_Q_PARAMS = {
    # General
    'NUM_INIT_GAMES': 10,  # number of games to play to gather initial data
    'NUM_TEST_GAMES': 10,  # number of games to run test on

    # Q Fitted DM
    'GAMMA': 0.3,
    'NUM_Q_FITTED_ITERATIONS': 2  # number of fitted q iterations to fit
    
}

# --- SARSA NNET Parameters -- #
SARSA_NN_PARAMS = {
    # params here
}
