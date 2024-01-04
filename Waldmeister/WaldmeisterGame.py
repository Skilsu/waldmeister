import numpy as np

from Game import Game
from Waldmeister.WaldmeisterLogic import WaldmeisterLogic

BOARD_SIZE = 5
COLOR_AMOUNT = 1


class WaldmeisterGame(Game):

    def __init__(self):
        super().__init__()
        self.game = WaldmeisterLogic(BOARD_SIZE, COLOR_AMOUNT)

    def getInitBoard(self):
        """
        Returns the initial game state including both the board and information about player's figures.
        :return: Tuple containing two np arrays -> (board_size x board_size x 9, 2 x 3 x 3)
        """
        # Initialize the board with zeros
        init_board = np.zeros((self.game.board_size, self.game.board_size, 9), dtype=int)

        # Initialize figure counts for both players
        figure_counts = np.full((2, 3, 3), self.game.color_amount, dtype=int)

        return init_board, figure_counts

    def getBoardSize(self):
        """
        Returns the necessary information about the size of both the board and the player's figures.
        :return: list of Integers: board_size, board_size, 9, 2, 3, 3
        """
        return self.game.board_size, self.game.board_size, 9, 2, 3, 3

    def getActionSize(self):
        return self.game.board_size * self.game.board_size * 9 * ((self.game.board_size - 1) * 3 + 1) + 1  # no plus 1??

    def getNextState(self, board, player, action):
        """
        executes move for given player
        :param board:
        :param player:
        :param action:
        :return:
        """
        # input checks
        if not np.array_equal(board, self.return_np_format()) or self.game.active_player == player:
            raise Exception
        if not 0 < action <= self.game.board_size * self.game.board_size * 9 * ((self.game.board_size - 1) * 3 + 1):
            raise ValueError

        # reset current player
        self.game.active_player = player

        # + 1 logic... not really useful?
        if action == self.game.board_size * self.game.board_size * 9 * ((self.game.board_size - 1) * 3 + 1):
            # TODO +1 Needed????
            return board, -player

        # calculating move
        moving = None
        if action >= self.game.board_size * self.game.board_size * 9:
            raw_move = action % ((self.game.board_size - 1) * 3)
            move_direction = int(raw_move / (self.game.board_size - 1))
            move_distance = raw_move % (self.game.board_size - 1)
            moving = [move_direction, move_distance]
            action = int(action / ((self.game.board_size - 1) * 3))
        elif not self.game.empty_board():
            # board should be empty if no move is provided
            raise ValueError

        # calculation of figure
        color = action % 9
        action_1 = action - color
        action_1 = action_1 / 9

        i = color // 3
        j = color % 3
        figure = [i, j]

        # calculation of starting position
        y = int(action_1) % self.game.board_size
        x = action_1 - y
        x = int(x / self.game.board_size)

        print(f"starting_from=[{x}, {y}], {figure=}, {moving=}, {action=}, {color=}, {x=}, {y=}")

        # execute move
        self.game.make_move(starting_from=[x, y], figure=figure, moving=moving)
        self.game.print_board()

        return self.return_np_format(), -player

    def getValidMoves(self, board, player):
        if not np.array_equal(board, self.return_np_format()) or self.game.active_player == player:
            raise Exception
        return super().getValidMoves(board, player)

    def getGameEnded(self, board, player):
        if not np.array_equal(board, self.return_np_format()) or self.game.active_player == player:
            raise Exception
        if self.game.has_legal_moves():
            return 0
        return self.game.is_winner(player)

    def getCanonicalForm(self, board, player):
        if not np.array_equal(board, self.return_np_format()) or self.game.active_player == player:
            raise Exception
        # TODO important for the order of the left available figures
        return super().getCanonicalForm(board, player)

    def getSymmetries(self, board, pi):
        if not np.array_equal(board, self.return_np_format()):
            raise Exception
        return super().getSymmetries(board, pi)

    def stringRepresentation(self, board):
        if not np.array_equal(board, self.return_np_format()):
            raise Exception
        return super().stringRepresentation(board)

    def return_np_format(self):
        board = np.full((self.game.board_size, self.game.board_size, 9), 0, dtype=object)

        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if self.game.field[i][j] is not None:
                    color, size = self.game.field[i][j]
                    figure_index = color * 3 + size
                    board[i, j, figure_index] = 1
        return board

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
    board, _ = test.getNextState(board, 0, 110)
    board, _ = test.getNextState(board, 0, 1403)
