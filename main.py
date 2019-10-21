import dramamanager
import player
import game
import policies

dm = dramamanager.DM()
player = player.Player(50, policies.policy1)
game = game.LotteryGame(dm, player, [0.40, 0.30, 0.1, 0.15, 0.05])

for i in range(100):
    done = game.step()

    if done:
        # do something
        print('done')
        break

    print('--')

3