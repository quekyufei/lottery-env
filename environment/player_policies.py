policy1 = {
    # ----- Enjoyment ----- #
    # General #
    'ENJOYMENT_DECAY_BASE': 1.05,
    'THRESHOLD_ENJOYMENT': 10,

    # tiers #
    'tiers': {
        'LOSS': -7,
        'SMALL_WIN': 10,
        'MED_WIN': 15,
        'LARGE_WIN': 20,
        'JACKPOT': 50
    },

    'BETTING_PROBABILITIES': [0.5, 0.3, 0.2],

    # Losing Streaks #
    'FRESH_LOSS_MULTIPLIER': 0.5,
    'THREE_LOSS_STREAK_MULTIPLIER': 1,
    'FIVE_LOSS_STREAK_MULTIPLIER': 1.5,
    'LARGE_LOSS_STREAK_MULTIPLIER': 1.7,

    # Winning Streaks #
    'FRESH_WIN_MULTIPLIER': 1,
    'THREE_WIN_MULTIPLIER': 1.2,
    'FIVE_WIN_MULTIPLIER': 1.5,
    'LARGE_WIN_STREAK_MULTIPLIER': 1,

    # Comeback #
    'COMEBACK_BASE': 1.2
}
