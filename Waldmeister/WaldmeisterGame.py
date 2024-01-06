import numpy as np

from Game import Game
from Waldmeister.WaldmeisterLogic import WaldmeisterLogic

BOARD_SIZE = 5
COLOR_AMOUNT = 1


class WaldmeisterGame(Game):

    def __init__(self):
        super().__init__()

    def getInitBoard(self):
        """
        Returns the initial game state including both the board and information about player's figures.
        :return: Tuple containing two np arrays -> (board_size x board_size x 9, 2 x 3 x 3)
        """
        # Initialize the board with zeros
        init_board = np.zeros((BOARD_SIZE, BOARD_SIZE, 9), dtype=int)

        # Initialize figure counts for both players
        figure_counts = np.zeros((2, 3, 3), dtype=int)

        return init_board, figure_counts

    def getBoardSize(self):
        """
        Returns the necessary information about the size of both the board and the player's figures.
        :return: list of Integers: board_size, board_size, 9, 2, 3, 3
        """
        return BOARD_SIZE, BOARD_SIZE, 9, 2, 3, 3

    def getActionSize(self):
        return (BOARD_SIZE * BOARD_SIZE * ((BOARD_SIZE - 1) * 3 + 1)) * 9 + 1  # no + 1???

    def getNextState(self, board, player, action):
        """
        executes move for given player
        :param board:
        :param player:
        :param action:
        :return:
        """
        game = self.get_game(board)

        if not 0 <= action <= BOARD_SIZE * BOARD_SIZE * 9 * ((BOARD_SIZE - 1) * 3 + 1):
            print(action)
            raise ValueError

        # + 1 logic... not really useful?
        if action == BOARD_SIZE * BOARD_SIZE * 9 * ((BOARD_SIZE - 1) * 3 + 1):
            # TODO +1 Needed????
            return board, -player

        starting_from, figure, moving = self.get_move_from_action(action)

        # execute move
        game.make_move(starting_from=starting_from, figure=figure, moving=moving, player=player)
        game.print_board()
        print(game.player)
        print("NextState worked")
        return self.return_np_format(game.field, game.player), -player

    def getValidMoves(self, board, player):
        game = self.get_game(board)
        value = int(game.empty_board())
        total_moves = [value for _ in range(BOARD_SIZE ** 2)]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                total_moves.extend(game.get_legal_moves_for_position([i, j]))
        print(len(total_moves), len(total_moves) / 13)

        legal_figures = []
        if player == -1:
            player = 0
        for i in game.player[player]:
            for j in i:
                if j == COLOR_AMOUNT:
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
        game = self.get_game(board)
        if game.has_legal_moves():
            return 0
        return game.is_winner(player)

    def getCanonicalForm(self, board, player):
        np_board, np_figures = board
        if player == -1:
            np_figures_swapped = np.swapaxes(np_figures, 1, 2)
            print(np_figures)  # TODO muss irgendwas
            print(np_figures_swapped)
            return np_board, np_figures_swapped
        return board

    def getSymmetries(self, board, pi):
        # No symmetries for now, return the original state and policy vector
        return [(board, pi)]

    def stringRepresentation(self, board):
        return self.get_game(board).get_str(player=1)

    @staticmethod
    def return_np_format(original_board, original_figures):

        board = np.zeros((BOARD_SIZE, BOARD_SIZE, 9), dtype=int)
        figures = np.zeros((2, 3, 3), dtype=int)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if original_board[i][j] is not None:
                    color, size = original_board[i][j]
                    figure_index = color * 3 + size
                    board[i, j, figure_index] = 1
        for i in range(2):
            for j in range(3):
                for k in range(3):
                    figures[i, j, k] = original_figures[i][j][k]
        return board, figures

    @staticmethod
    def get_move_from_action(action):
        # calculation of figure
        color = action % 9
        action = int(action / 9)
        i = color // 3
        j = color % 3
        figure = [i, j]

        # calculating move
        moving = None
        if action >= BOARD_SIZE ** 2:
            raw_move = action % ((BOARD_SIZE - 1) * 3)
            move_direction = int(raw_move / (BOARD_SIZE - 1))
            move_distance = raw_move % (BOARD_SIZE - 1)
            moving = [move_direction, move_distance]
            action = int(action / ((BOARD_SIZE - 1) * 3))

        # calculation of starting position
        y = int(action) % BOARD_SIZE
        x = action - y
        x = int(x / BOARD_SIZE)

        print(f"starting_from=[{x}, {y}], {figure=}, {moving=}, {action=}, {color=}, {x=}, {y=}")
        return [x, y], figure, moving

    def get_game(self, board):
        original_board, original_figures = self.convert_to_original_format(board)

        game = WaldmeisterLogic(BOARD_SIZE, COLOR_AMOUNT)
        game.field = original_board
        game.player = original_figures
        return game

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
                    print(f"{i=}, {j=}, {k=}, {np_figures=}")
                    original_format_figures[i][j][k] = int(np_figures[i, j, k])

        return original_format_board, original_format_figures


if __name__ == "__main__":
    test = WaldmeisterGame()
    board = test.getInitBoard()
    WaldmeisterLogic(BOARD_SIZE, COLOR_AMOUNT).print_board()
    board, player = test.getNextState(board, 1, 110)
    board, player = test.getNextState(board, player, 1403)
    test.getValidMoves(board, player)
