import numpy as np

from Game import Game
from Waldmeister.WaldmeisterLogic import WaldmeisterLogic

BOARD_SIZE = 5
COLOR_AMOUNT = 1


class WaldmeisterGame(Game):

    def getInitBoard(self):
        """
        Field should be the normal field board_size x board_size with the 9 figures (3 colors x 3 sizes).
        :return:
        board as 3D np array with dimensions -> board_size x board_size x 9
        """
        game = WaldmeisterLogic(BOARD_SIZE, COLOR_AMOUNT)
        start_board = np.full((game.board_size, game.board_size, 9), None, dtype=object)
        return start_board

    def getBoardSize(self):
        game = WaldmeisterLogic(BOARD_SIZE, COLOR_AMOUNT)
        return game.board_size, game.board_size, 9

    def getActionSize(self):
        game = WaldmeisterLogic(BOARD_SIZE, COLOR_AMOUNT)
        return game.board_size * game.board_size * 9 * ((game.board_size - 1) * 3 + 1) + 1  # no plus 1???

    def getNextState(self, board, player, action):
        game = WaldmeisterLogic(BOARD_SIZE, COLOR_AMOUNT)

        if action == game.board_size * game.board_size * 9 * ((game.board_size - 1) * 3 + 1):
            return board, -player

        # TODO from here...
        board = d
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action / self.n), action % self.n)
        b.execute_move(move, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        return super().getValidMoves(board, player)

    def getGameEnded(self, board, player):
        return super().getGameEnded(board, player)

    def getCanonicalForm(self, board, player):
        return super().getCanonicalForm(board, player)

    def getSymmetries(self, board, pi):
        return super().getSymmetries(board, pi)

    def stringRepresentation(self, board):
        return super().stringRepresentation(board)

