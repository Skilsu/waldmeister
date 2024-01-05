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
        figure_counts = np.zeros((2, 3, 3), dtype=int)

        return init_board, figure_counts

    def getBoardSize(self):
        """
        Returns the necessary information about the size of both the board and the player's figures.
        :return: list of Integers: board_size, board_size, 9, 2, 3, 3
        """
        return self.game.board_size, self.game.board_size, 9, 2, 3, 3

    def getActionSize(self):
        return (self.game.board_size * self.game.board_size * ((self.game.board_size - 1) * 3 + 1)) * 9 + 1  # no + 1???

    def getNextState(self, board, player, action):
        """
        executes move for given player
        :param board:
        :param player:
        :param action:
        :return:
        """
        self.check_inputs(board, player)
        if not 0 < action <= self.game.board_size * self.game.board_size * 9 * ((self.game.board_size - 1) * 3 + 1):
            raise ValueError

        # + 1 logic... not really useful?
        if action == self.game.board_size * self.game.board_size * 9 * ((self.game.board_size - 1) * 3 + 1):
            # TODO +1 Needed????
            return board, -player

        starting_from, figure, moving = self.get_move_from_action(action)

        # execute move
        self.game.make_move(starting_from=starting_from, figure=figure, moving=moving)
        self.game.print_board()

        return self.return_np_format(), -player

    def getValidMoves(self, board, player):
        self.check_inputs(board, player)
        value = int(self.game.empty_board())
        total_moves = [value for _ in range(self.game.board_size ** 2)]
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                total_moves.extend(self.game.get_legal_moves_for_position([i, j]))
        print(len(total_moves), len(total_moves) / 13)

        legal_figures = []
        if player == -1:
            player = 0
        for i in self.game.player[player]:
            for j in i:
                if j == self.game.color_amount:
                    legal_figures.append(0)
                else:
                    legal_figures.append(1)

        total_moves_figures = []
        for i in total_moves:
            for j in legal_figures:
                if i == j == 1:
                    total_moves_figures.append(1)
                else:
                    total_moves_figures.append(0)

        print(len(total_moves_figures), len(total_moves_figures) / 9)
        total_moves_figures.append(0)
        ones = list(filter(lambda x: x == 1, total_moves_figures))
        print(len(ones))
        return total_moves_figures

    def getGameEnded(self, board, player):
        self.check_inputs(board, player)  # ???
        if self.game.has_legal_moves():
            return 0
        return self.game.is_winner(player)

    def getCanonicalForm(self, board, player):
        self.check_inputs(board, -self.game.active_player)
        # TODO important for the order of the left available figures
        return super().getCanonicalForm(board, player)

    def getSymmetries(self, board, pi):
        self.check_inputs(board, -self.game.active_player)
        return super().getSymmetries(board, pi)

    def stringRepresentation(self, board):
        self.check_inputs(board, -self.game.active_player)
        return super().stringRepresentation(board)

    def return_np_format(self):
        board = np.zeros((self.game.board_size, self.game.board_size, 9), dtype=int)
        figures = np.zeros((2, 3, 3), dtype=int)
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if self.game.field[i][j] is not None:
                    color, size = self.game.field[i][j]
                    figure_index = color * 3 + size
                    board[i, j, figure_index] = 1
        for i in range(2):
            for j in range(3):
                for k in range(3):
                    figures[i, j, k] = self.game.player[i][j][k]
        return board, figures

    def get_move_from_action(self, action):
        # calculation of figure
        color = action % 9
        action = int(action / 9)
        i = color // 3
        j = color % 3
        figure = [i, j]

        # calculating move
        moving = None
        if action >= self.game.board_size * self.game.board_size:
            raw_move = action % ((self.game.board_size - 1) * 3)
            move_direction = int(raw_move / (self.game.board_size - 1))
            move_distance = raw_move % (self.game.board_size - 1)
            moving = [move_direction, move_distance]
            action = int(action / ((self.game.board_size - 1) * 3))
        elif not self.game.empty_board():
            # board should be empty if no move is provided
            raise ValueError

        # calculation of starting position
        y = int(action) % self.game.board_size
        x = action - y
        x = int(x / self.game.board_size)

        print(f"starting_from=[{x}, {y}], {figure=}, {moving=}, {action=}, {color=}, {x=}, {y=}")
        return [x, y], figure, moving

    @staticmethod
    def convert_to_original_format(boards):
        np_board, np_figures = boards

        board_size, _, num_figures = np_board.shape

        original_format_board = [[None for _ in range(board_size)] for _ in range(board_size)]
        original_format_figures = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(2)]

        for i in range(board_size):
            for j in range(board_size):
                for k in range(num_figures):
                    if np_board[i, j, k] != 0:
                        # Extract color and size from the figure index
                        color = k // 3
                        size = k % 3
                        original_format_board[i][j] = [color, size]
                        break

        for i in range(2):
            for j in range(3):
                for k in range(3):
                    original_format_figures[i][j][k] = int(np_figures[i, j, k])

        return original_format_board, original_format_figures

    def check_inputs(self, board, player=None):
        # input checks
        np_board, np_figures = board
        original_board, original_figures = self.return_np_format()
        e = ValueError()
        if not np.array_equal(np_board, original_board):
            e.add_note("Board doesn't match stored version")
            raise e
        elif not np.array_equal(np_figures, original_figures):
            e.add_note("Figures doesn't match stored version")
            raise e
        elif self.game.active_player == player:
            e.add_note(f"Wrong player provided. Got: {player}, expected: {-self.game.active_player} (or None)")
            raise e


if __name__ == "__main__":
    test = WaldmeisterGame()
    board = test.getInitBoard()
    WaldmeisterLogic(BOARD_SIZE, COLOR_AMOUNT).print_board()
    board, player = test.getNextState(board, 1, 110)
    # board, player = test.getNextState(board, player, 1403)
    test.getValidMoves(board, player)
