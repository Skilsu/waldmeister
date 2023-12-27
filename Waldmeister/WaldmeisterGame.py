import numpy as np

from Game import Game
from Waldmeister.WaldmeisterLogic import Board

class WaldmeisterGame(Game):

    def __init__(self, n=8, color_amount=3):
        super().__init__()
        self.n = n

        self.color_amount = color_amount
        self.game_pieces_players = [[[0 for _ in range(color_amount)] for _ in range(color_amount)] for _ in range(2)]
        """for i in range(len(self.game_pieces_players[1])):
            for j in range(len(self.game_pieces_players[1][i])):
                self.game_pieces_players[1][i][j] = 2"""

        self.pieces = [[None for _ in range(n)] for _ in range(n)]
        self.active_start = None
        self.active_end = None
        self.empty_board = True
        self.active_player = 0  # can be 0 or 1 to access over self.player

    def getInitBoard(self):
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        return (self.n, self.n)

    def getActionSize(self):
        return self.n*self.n*2 + self.color_amount*self.color_amount + 1  # no plus 1???

    def getNextState(self, board, player, action):

        if action == self.n*self.n*2 + self.color_amount*self.color_amount:
            return (board, -player)
        #board = d
        #b = Board(self.n)
        #b.pieces = np.copy(board)
        #move = (int(action / self.n), action % self.n)
        #b.execute_move(move, player)
        #return (b.pieces, -player)

    def getValidMoves(self, board, player):
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves(player)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)


        # die spieler haben noch steine zu spielen
        if b.has_legal_moves(self.game_pieces_players):
            return 0

        return b.is_win(player)




    def getCanonicalForm(self, board, player):
        return board # player is not so important?

    def getSymmetries(self, board, pi):
        return super().getSymmetries(board, pi)

    def stringRepresentation(self, board):
        return super().stringRepresentation(board)

    @staticmethod
    def display(board):
        x = -4
        y = 3
        for i in range(15):
            line_str = ""
            old_x = x
            old_y = y
            for j in range(15):
                x += 0.5
                y += 0.5
                if 0 <= x < 8 and 0 <= y < 8 and y == int(y) and x == int(x):

                    line_str = line_str + str(board[int(x)][int(y)])
                else:
                    line_str = line_str + "    "
            print(line_str)
            x = old_x + 0.5
            y = old_y - 0.5

        # zeilen und spaltenindex
        # Determine the maximum width needed for any cell
        max_cell_width = max((len(str(item)) for row in board for item in row if item is not None), default=len('None'))
        max_cell_width = max(max_cell_width, len("None"))

        # Print column headers with padding to match the cell width
        print("    ", end="")
        for col in range(len(board[0])):
            print(f" {col:^{max_cell_width}}", end="")
        print("\n" + "    " + "-" * (max_cell_width + 1) * len(board[0]))

        # Print rows with row index
        for row in range(len(board)):
            print(f"{row} |", end="")
            for col in range(len(board[0])):
                # Convert the element to a string for consistent formatting
                element = str(board[row][col]) if board[row][col] is not None else 'None'
                print(f" {element:^{max_cell_width}}", end="")
            print()





if __name__ == "__main__":
    game = WaldmeisterGame()
    from WaldmeisterLogic import Board
    b = Board()
    b.pieces[0][0] = [2,1]
    game.display(b)


