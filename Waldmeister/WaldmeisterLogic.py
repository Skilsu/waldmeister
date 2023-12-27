"""
Board class.
Bord data:

"""

# static number of Fields available in Waldmeister 64
NUMBER_OF_FIELDS = 64

class Board:

    def __init__(self, n=8):
        self.n = n
        self.pieces = [[None for _ in range(n)] for _ in range(n)]

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pieces[index]

    def is_win(self, curPlayer):

        if curPlayer < 0:
            curPlayer = 1
            otherPlayer = 0
        elif curPlayer > 0:
            curPlayer = 0
            otherPlayer = 1
        p1 = self.count_points(curPlayer)
        p2 = self.count_points(otherPlayer)
        if p1 > p2:
            return 1
        elif p2 > p1:
            return -1
        # draw has a very little value
        return 1e-4

    def has_legal_moves(self, game_pieces_players):

        for i in game_pieces_players:
            for j in i:
                for k in j:
                    if k != 2:
                        return True
        return False

    def get_legal_moves(self, curPlayer):
        if curPlayer < 0:
            curPlayer = 1
            otherPlayer = 0
        elif curPlayer > 0:
            curPlayer = 0
            otherPlayer = 1


    def count_points(self, player_number):
        points = 0
        for i in range(3):
            points += self.count_points_per_layer(player_number, i)
        return points

    def count_points_per_layer(self, player_number, layer):
        boards = self.get_cleaned_boards_per_player_per_layer(player_number, layer)
        res = 0
        for board in boards:
            board_result = 0
            for row in board:
                for entry in row:
                    board_result += entry
            res = max(res, board_result)
        return res

    def get_cleaned_boards_per_player_per_layer(self, player_number, layer):
        boards = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(self._get_reward_board([i, j]))
            boards.append(row)

        if player_number == 0:
            added_board = boards[0][layer]
            for i in range(1, 3):
                for jdx, j in enumerate(boards[i][layer]):
                    for kdx, k in enumerate(j):
                        if k == 1:
                            added_board[jdx][kdx] = 1
        else:
            added_board = boards[layer][0]
            for i in range(1, 3):
                for jdx, j in enumerate(boards[layer][i]):
                    for kdx, k in enumerate(j):
                        if k == 1:
                            added_board[jdx][kdx] = 1

        return self.evaluate_boards(added_board)

    def _get_reward_board(self, symbol):
        counted_points = []
        for i in self.pieces:
            row_count = []
            for j in i:
                if j == symbol:
                    row_count.append(1)
                else:
                    row_count.append(0)
            counted_points.append(row_count)
        return counted_points

    def evaluate_board(self, board, position):
        evaluated_board = []
        found_pattern = [[0 for _ in range(8)] for _ in range(8)]
        evaluated_pattern = [[0 for _ in range(8)] for _ in range(8)]
        evaluated_pattern[position[0]][position[1]] = 1
        while found_pattern != evaluated_pattern:
            evaluated_board = []
            found_pattern = [row[:] for row in evaluated_pattern]
            for i in range(8):
                evaluated_row = []
                for j in range(8):
                    if [i, j] != position and board[i][j] == 1 and (
                            (i > 0 and evaluated_pattern[i - 1][j] == 1) or
                            (i < 7 and evaluated_pattern[i + 1][j] == 1) or
                            (j > 0 and evaluated_pattern[i][j - 1] == 1) or
                            (j < 7 and evaluated_pattern[i][j + 1] == 1) or
                            (i > 0 and 7 > j and evaluated_pattern[i - 1][j + 1] == 1)):
                        evaluated_row.append(1)
                    else:
                        if [i, j] != position:
                            evaluated_row.append(0)
                        else:
                            evaluated_row.append(1)
                evaluated_board.append(evaluated_row)
            evaluated_pattern = [row[:] for row in evaluated_board]
        return evaluated_board

    def evaluate_boards(self, board):
        boards = []
        for kdx, k in enumerate(board):
            for ldx, l in enumerate(k):
                if l == 1:
                    evaluated_board = self.evaluate_board(board, [kdx, ldx])
                    for idx, i in enumerate(board):
                        for jdx, _ in enumerate(i):
                            if evaluated_board[idx][jdx] == 1:
                                board[idx][jdx] = 0
                    boards.append(evaluated_board)
        '''
        # might not be needed???????
        unique_boards = set()
        for board in boards:
            # Convert the board to a tuple since lists are not hashable and cannot be added to a set
            board_tuple = tuple(map(tuple, board))
            unique_boards.add(board_tuple)
        # Convert the unique boards back to a list of lists
        boards = [list(board_tuple) for board_tuple in unique_boards]
        '''
        return boards