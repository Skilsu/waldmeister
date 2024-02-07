import logging

from MCTS import MCTS
from Waldmeister.keras.NNet import NNetWrapper as NNet

import numpy as np
from utils import *

log = logging.getLogger(__name__)

"""
Random and Human-ineracting players for the game of Waldmeister.

Author: Abdülkerim Kilinc, github.com/AbdulkerimKilinc
Author: Nicolas Henrich, github.com/Skilsu

Date: Jan 12, 2024.

Based on the OthelloPlayers by Surag Nair.
"""

class RandomPlayer:
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanWaldmeisterPlayer:
    def __init__(self, game):
        self.game = game

    def play(self, board):
        log.error("Not implemented! Use PygameGui instead!")
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        for i in range(len(valid)):
            if valid[i]:
                log.error("Not implemented! Use PygameGui instead!")
        while True:
            # Python 3.x
            a = input()
            # Python 2.x
            # a = raw_input()

            x, y = [int(x) for x in a.split(' ')]
            a = self.game.n * x + y if x != -1 else self.game.n ** 2
            if valid[a]:
                break
            else:
                log.error('Invalid action! Insert again.')

        return a


class AiWaldmeisterPlayer:
    def __init__(self, game, filename):
        n1 = NNet(game)
        n1.load_checkpoint('./pretrained_models/Waldmeister/pytorch/', filename)
        args1 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
        self.mcts1 = MCTS(game, n1, args1)

    def play(self, board):
        return np.argmax(self.mcts1.getActionProb(board, temp=0))
