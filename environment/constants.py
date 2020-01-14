import numpy as np

##########################
# --- lotterygame.py --- #
##########################

# Lottery

WIN_CHANCE = 0.60
LOSS_CHANCE = 1 - WIN_CHANCE

# Ratio of winning -- small : med : large : jackpot
RELATIVE_WINNING_RATIOS = np.array([30, 15, 10, 5])

# Probability Modifiers #
SMALL_INC_WIN_PROB = 0.05
LARGE_INC_WIN_PROB = 0.20
SMALL_DEC_WIN_PROB = -0.05
LARGE_DEC_WIN_PROB = -0.20
PROBABILITY_MODIFIER_MULTIPLIER = [0, SMALL_INC_WIN_PROB, LARGE_INC_WIN_PROB, SMALL_DEC_WIN_PROB, LARGE_DEC_WIN_PROB]  # index 0 is for doing nothing

MIN_PROBABILITY = 0.01


# Winnings

WINNING_MULTIPLIER = [
    0.0,  # Loss
    1.0,  # Small Win
    2.0,  # Medium Win
    5.0,  # Large Win
    20.0  # Jackpot
]


# DM Actions

WEIGHTED_ACTION_PROBS = [0.4, 0.15, 0.15, 0.15, 0.15]


########################
# --- plotpoint.py --- #
########################

LOTTERY_RESULTS = ['LOSS', 'SMALL_WIN', 'MED_WIN', 'LARGE_WIN', 'JACKPOT']
