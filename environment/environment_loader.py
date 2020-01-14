from . import lotterygame
from . import playerclass
from . import player_policies


def load_lottery_game(verbosity):
    player = playerclass.Player(player_policies.policy1, verbose=verbosity)
    game = lotterygame.LotteryGame(player, verbose=verbosity)
    return game
