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

    def get_legal_moves(self, empty_board, game_pieces_players, curPlayer):
        if curPlayer < 0:
            curPlayer = 1
            otherPlayer = 0
        elif curPlayer > 0:
            curPlayer = 0
            otherPlayer = 1

        legal_moves = []
        all_moves = []
        legal_moves_binary = []

        game_pieces_curPlayer = game_pieces_players[curPlayer]

        game_pieces = self.get_game_pieces_as_list(game_pieces_curPlayer)


        # leeres Feld => erster Zug
        if empty_board:
            for piece in game_pieces:
                moves, moves_binary = self.get_moves(piece)
                legal_moves.extend(moves)
                legal_moves_binary.extend(moves_binary)
            return legal_moves, legal_moves_binary


        # ab hier wenn schon figuren auf feld sind => zweiter Zug...



    def get_moves(self, piece):
        """
        Generate all possible moves for a given piece.
        :param piece: (list) A two-element list representing the piece, where
                  piece[0] is the height (0-2) and piece[1] is the color (0-2).
        :return: A tuple containing two lists. The first list contains the standard
                representation of all possible moves for the piece, and the second
                list contains the binary representation of these moves.
        """
        board_locations = self.get_board_locations()
        moves = []
        moves_binary = []
        for location in board_locations:
            move = [piece, location]
            move_binary = self.create_binary_move(piece, location)
            moves.append(move)
            moves_binary.append(move_binary)

        return moves, moves_binary

    def create_binary_move(self, piece, location):
        """
        Create a binary representation of a move.
        :param piece: (list) A two-element list representing the piece, where
                          piece[0] is the height (0-2) and piece[1] is the color (0-2).
        :param location: (list) A two-element list representing the board location,
                             where location[0] is the row and location[1] is the column.
        :return: (list) A binary vector representing the move. The first 9 elements represent
                  the piece type, and the next 64 elements represent the board position.
        """

        height, color = piece
        piece_type = height * 3 + color  # Convert height and color into a single index
        piece_binary = [0] * 9
        piece_binary[piece_type] = 1

        # Convert board location to a single index
        location_index = location[0] * 8 + location[1]
        location_binary = [0] * 64
        location_binary[location_index] = 1

        return piece_binary + location_binary




    def get_game_pieces_as_list(self, game_pieces_curPlayer):
        """
        Convert the game pieces of the current player into a list format.

        This method processes the game pieces of the current player, represented as a 2D array where
        each element indicates the number of times a specific piece has been played (maximum of 2).
        It converts this array into a list of pieces, where each piece is represented by its height and color.

        :param game_pieces_curPlayer: (list) A 2D list representing the current player's game pieces.
                                    Each element is an integer indicating how many times that specific
                                    piece has been played.
        :return: A list of pieces, where each piece is represented as a list [height, color],
                with 'height' and 'color' indicating the piece's characteristics.
        """
        return [[idx, jdx] for idx, row in enumerate(game_pieces_curPlayer)
                for jdx, piece in enumerate(row) if piece < 3]

    def get_board_locations(self):
        """
        Generate a list of all possible board locations.
        This method creates a list of all possible locations on the game board. Each location
        is represented as a list [x, y], where 'x' is the row index and 'y' is the column index.
        :return:
        """
        list = []
        for idx, i in enumerate(self.pieces):
            for jdx, j in enumerate(i):
                list.append([idx, jdx])
        return list

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