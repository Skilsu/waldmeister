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
        start_board = np.full((game.board_size, game.board_size, 9), 0, dtype=object)
        return start_board

    def getBoardSize(self):
        game = WaldmeisterLogic(BOARD_SIZE, COLOR_AMOUNT)
        return game.board_size, game.board_size, 9

    def getActionSize(self):
        game = WaldmeisterLogic(BOARD_SIZE, COLOR_AMOUNT)
        return game.board_size * game.board_size * 9 * ((game.board_size - 1) * 3 + 1) + 1  # no plus 1???

    def getNextState(self, board, player, action):
        """

        :param board:
        :param player:
        :param action:
        :return:
        """
        game = WaldmeisterLogic(BOARD_SIZE, COLOR_AMOUNT)
        game.field = self.convert_to_original_format(board)

        if action == game.board_size * game.board_size * 9 * ((game.board_size - 1) * 3 + 1):  # TODO Needed????
            return board, -player

        moving = None
        if action >= game.board_size * game.board_size * 9:
            raw_move = action % ((game.board_size - 1) * 3)
            move_direction = int(raw_move / (game.board_size - 1))  # TODO issue! doesnt work correctly
            move_distance = raw_move % (game.board_size - 1)
            moving = [move_direction, move_distance]
            action = int(action / ((game.board_size - 1) * 3))
        elif not game.empty_board():
            raise ValueError
        color = action % 9
        action_1 = action - color
        action_1 = action_1 / 9
        y = int(action_1) % game.board_size
        x = action_1 - y
        x = int(x / game.board_size)
        i = color // 3
        j = color % 3
        figure = [i, j]
        print(f"{action=}, {moving=}, {color=}, {figure=}, {y=}, {x=}")

        game.make_move(starting_from=[x, y], figure=figure, moving=moving)
        game.print_board()

        num_figures = 9  # Assuming 3 colors x 3 sizes
        board = np.full((game.board_size, game.board_size, num_figures), 0, dtype=object)

        for i in range(game.board_size):
            for j in range(game.board_size):
                if game.field[i][j] is not None:
                    color, size = game.field[i][j]
                    figure_index = color * 3 + size
                    board[i, j, figure_index] = 1

        return board, -player

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

    @staticmethod
    def convert_to_original_format(np_board):
        board_size, _, num_figures = np_board.shape
        original_format_board = [[None for _ in range(board_size)] for _ in range(board_size)]

        for i in range(board_size):
            for j in range(board_size):
                for k in range(num_figures):
                    if np_board[i, j, k] != 0:
                        # Extract color and size from the figure index
                        color = k // 3
                        size = k % 3
                        original_format_board[i][j] = [color, size]
                        break

        return original_format_board


if __name__ == "__main__":
    test = WaldmeisterGame()
    board = test.getInitBoard()
    WaldmeisterLogic(BOARD_SIZE, COLOR_AMOUNT).print_board()
    board, _ = test.getNextState(board, 0, 80)
    board, _ = test.getNextState(board, 0, 911)
