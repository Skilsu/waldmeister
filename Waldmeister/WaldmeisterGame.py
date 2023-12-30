import numpy as np

from Game import Game


class WaldmeisterGame(Game):

    def getInitBoard(self):
        return_field = []
        for i in self.field:
            for _ in i:
                return_field.append(0)
        return np.array(return_field)

    def getBoardSize(self):
        return (self.board_size, self.board_size)

    def getActionSize(self):
        return self.board_size * self.board_size * 2 + self.color_amount * self.color_amount + 1  # no plus 1???

    def getNextState(self, board, player, action):

        if action == self.board_size * self.board_size * 2 + self.color_amount * self.color_amount:
            return (board, -player)
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

