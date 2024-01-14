import Arena
from MCTS import MCTS
from Waldmeister.WaldmeisterGame import WaldmeisterGame
from Waldmeister.WaldmeisterPlayers import AiWaldmeisterPlayer
from Waldmeister.keras.NNet import NNetWrapper as NNet

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

human_vs_cpu = False

g = WaldmeisterGame()


# nnet players
n1p = AiWaldmeisterPlayer(g, 'best_nico_5.h5').play

n2 = NNet(g)
n2.load_checkpoint('./pretrained_models/Waldmeister/pytorch/', 'best_nico_5.h5')
args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
mcts2 = MCTS(g, n2, args2)
n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

arena = Arena.Arena(n1p, player2, g, display=WaldmeisterGame.display)
print(arena.playGames(2, verbose=True))
