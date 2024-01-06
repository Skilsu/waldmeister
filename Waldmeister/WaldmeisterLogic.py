"""
Board class.
Bord data:

"""


class WaldmeisterLogic:

    def __init__(self, board_size=8, color_amount=3):
        super().__init__()
        try:
            if board_size < 5:
                raise ValueError
        except ValueError as e:
            e.add_note("Number too low! Needs to be at least 5")
            raise e
        while color_amount * 18 > board_size ** 2:
            color_amount -= 1
            print(f"WARNING: color_amount needed to be adjusted from {color_amount + 1} to {color_amount} bc it was "
                  f"too high!")
        self.board_size = board_size
        self.color_amount = color_amount
        self.player = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(2)]
        self.field = [[None for _ in range(board_size)] for _ in range(board_size)]


    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.field[index]

    def get_str(self, player, active_position=None):
        x = -(self.board_size / 2)
        y = (self.board_size / 2) - 1
        if active_position is None:
            active_position = [-1, -1]
        active_positions = self.get_active_positions(active_position)
        full_str = ""
        for i in range(self.board_size * 2 - 1):
            line_str = ""
            old_x = x
            old_y = y
            for j in range(self.board_size * 2 - 1):
                x += 0.5
                y += 0.5
                if 0 <= x < self.board_size and 0 <= y < self.board_size and y == int(y) and x == int(x):
                    if x == active_position[0] and y == active_position[1]:
                        if self.field[int(x)][int(y)] is None:
                            line_str = line_str + "\u0332".join(" None ")
                        else:
                            line_str = line_str + "\u0332".join(str(self.field[int(x)][int(y)]))
                    elif active_position is not None and active_positions[int(x)][int(y)] == 1:
                        line_str = line_str + str("Active")
                    elif self.field[int(x)][int(y)] is None:
                        line_str = line_str + " None "
                    else:
                        line_str = line_str + str(self.field[int(x)][int(y)])
                else:
                    line_str = line_str + "      "
            full_str = full_str + line_str + "\n"
            x = old_x + 0.5
            y = old_y - 0.5
        for i in range(3):
            if player == 1:
                full_str = (full_str + f" {self.color_amount - self.player[1][i][0]} "
                                       f"{self.color_amount - self.player[1][i][1]} "
                                       f"{self.color_amount - self.player[1][i][2]}" +
                            "                                         " +
                            f" {self.color_amount - self.player[0][i][0]} "
                            f"{self.color_amount - self.player[0][i][1]} "
                            f"{self.color_amount - self.player[0][i][2]}\n")
            else:
                full_str = (full_str + f" {self.color_amount - self.player[0][i][0]} "
                                       f"{self.color_amount - self.player[0][i][1]} "
                                       f"{self.color_amount - self.player[0][i][2]}" +
                            "                                         " +
                            f" {self.color_amount - self.player[1][i][0]} "
                            f"{self.color_amount - self.player[1][i][1]} "
                            f"{self.color_amount - self.player[1][i][2]}\n")
        return full_str

    def print_board(self, active_position=None):
        print(self.get_str(player=1, active_position=active_position))

    @staticmethod
    def get_move_position(starting_from, moving):
        moving_to = [starting_from[0], starting_from[1]]
        if moving[0] == 0:
            if moving[1] < starting_from[0]:
                moving_to[0] = moving[1]
            else:
                moving_to[0] = moving[1] + 1
        elif moving[0] == 1:
            if moving[1] < starting_from[1]:
                moving_to[1] = moving[1]
            else:
                moving_to[1] = moving[1] + 1
        else:
            if moving[1] < starting_from[1]:

                moving_to[1] = moving[1]
                moving_to[0] += starting_from[1] - moving_to[1]
            else:
                moving_to[1] = moving[1] + 1
                moving_to[0] += starting_from[1] - moving_to[1]
        return moving_to

    def get_legal_moves_for_position(self, starting_from):
        if self.field[starting_from[0]][starting_from[1]] is None:
            return [0 for _ in range(3 * (self.board_size - 1))]
        possible_moves = self.get_active_positions(starting_from)
        moves_1 = []
        for i in possible_moves:
            moves_1.append(i[starting_from[1]])
        moves_2 = possible_moves[starting_from[0]]
        moves_3 = []
        x = starting_from[0] + starting_from[1]
        y = 0
        for i in range(starting_from[0] + starting_from[1] + 1):
            if 0 <= x < self.board_size and 0 <= y < self.board_size:
                moves_3.append(possible_moves[x][y])
            x -= 1
            y += 1
        while len(moves_3) < len(moves_2):
            moves_3.append(0)
        moves_1.remove(1)
        moves_2.remove(1)
        moves_3.remove(1)
        moves = moves_1
        moves.extend(moves_2)
        moves.extend(moves_3)
        return moves

    def make_move(self, starting_from, figure, player, moving_to=None, moving=None):
        # handle player position
        if player == -1:
            player = 0
        else:
            player = 1

        if moving:
            moving_to = self.get_move_position(starting_from, moving)

        # Validate if passed figure is still available for player
        if self.player[player][figure[0]][figure[1]] >= self.color_amount:
            return ValueError  # TODO good practise???

        # add figure to played figures
        self.player[player][figure[0]][figure[1]] += 1

        # add figure to board (first round)
        if self.empty_board() and self.field[starting_from[0]][starting_from[1]] is None:
            self.field[starting_from[0]][starting_from[1]] = figure

        # add figure to board (not first round)
        elif (self.field[moving_to[0]][moving_to[1]] is None
              and self.field[starting_from[0]][starting_from[1]] is not None):
            self.field[moving_to[0]][moving_to[1]] = self.field[starting_from[0]][starting_from[1]]
            self.field[starting_from[0]][starting_from[1]] = figure

    def empty_board(self):
        for i in self.field:
            for j in i:
                if j is not None:
                    return False
        return True

    def get_active_positions(self, active_position):
        """
        find active positions to draw allowed lines.
        """
        if active_position is None or self.field[active_position[0]][active_position[1]] is None:
            return [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        active_positions = []
        for i in range(self.board_size):
            active_row = []
            for j in range(self.board_size):
                if (i == active_position[0]
                        or j == active_position[1]
                        or active_position[1] + active_position[0] == i + j):
                    active_row.append(1)
                else:
                    active_row.append(0)
            active_positions.append(active_row)

        x = active_position[0]
        toggle = False
        while x > 0:
            x -= 1
            if self.field[x][active_position[1]] is not None or toggle:
                toggle = True
                active_positions[x][active_position[1]] = 0
        x = active_position[0]
        toggle = False
        while x < self.board_size - 1:
            x += 1
            if self.field[x][active_position[1]] is not None or toggle:
                toggle = True
                active_positions[x][active_position[1]] = 0
        y = active_position[1]
        toggle = False
        while y > 0:
            y -= 1
            if self.field[active_position[0]][y] is not None or toggle:
                toggle = True
                active_positions[active_position[0]][y] = 0
        y = active_position[1]
        toggle = False
        while y < self.board_size - 1:
            y += 1
            if self.field[active_position[0]][y] is not None or toggle:
                toggle = True
                active_positions[active_position[0]][y] = 0

        x = active_position[0]
        y = active_position[1]
        toggle = False
        while y > 0 and x < self.board_size - 1:
            y -= 1
            x += 1
            if self.field[x][y] is not None or toggle:
                toggle = True
                active_positions[x][y] = 0
        x = active_position[0]
        y = active_position[1]
        toggle = False
        while y < self.board_size - 1 and x > 0:
            y += 1
            x -= 1
            if self.field[x][y] is not None or toggle:
                toggle = True
                active_positions[x][y] = 0

        return active_positions

    def winner(self):
        if self.has_legal_moves():
            return 0
        return self.is_winner(1)

    def is_winner(self, current_player):
        p1 = self.count_points(current_player)
        p2 = self.count_points(-current_player)
        if p1 > p2:
            return 1  # win
        elif p2 > p1:
            return -1  # loss
        return 1e-4  # draw

    def has_legal_moves(self):
        for i in self.player:
            for j in i:
                for k in j:
                    if k != self.color_amount:
                        return True
        return False

    def get_legal_moves(self, empty_board, game_pieces_players, current_player):
        if current_player == -1:
            current_player = 0

        legal_moves = []
        all_moves = []
        legal_moves_binary = []

        game_pieces_current_player = game_pieces_players[current_player]

        game_pieces = self.get_game_pieces_as_list(game_pieces_current_player)

        # leeres Feld => erster Zug
        if empty_board:
            for piece in game_pieces:
                moves, moves_binary = self.get_moves(piece)
                legal_moves.extend(moves)
                legal_moves_binary.extend(moves_binary)
            return legal_moves, legal_moves_binary

        # ab hier wenn schon figuren auf feld sind → zweiter Zug...

    def get_moves_old(self, piece):
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
        for idx, i in enumerate(self.field):
            for jdx, j in enumerate(i):
                list.append([idx, jdx])
        return list

    def count_points(self, player_number):
        if player_number == -1:
            player_number = 0
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
        for i in self.field:
            row_count = []
            for j in i:
                if j == symbol:
                    row_count.append(1)
                else:
                    row_count.append(0)
            counted_points.append(row_count)
        return counted_points

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

    def evaluate_board(self, board, position):
        evaluated_board = []
        found_pattern = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        evaluated_pattern = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        evaluated_pattern[position[0]][position[1]] = 1
        while found_pattern != evaluated_pattern:
            evaluated_board = []
            found_pattern = [row[:] for row in evaluated_pattern]
            for i in range(self.board_size):
                evaluated_row = []
                for j in range(self.board_size):
                    if [i, j] != position and board[i][j] == 1 and (
                            (i > 0 and evaluated_pattern[i - 1][j] == 1) or
                            (i < self.board_size - 1 and evaluated_pattern[i + 1][j] == 1) or
                            (j > 0 and evaluated_pattern[i][j - 1] == 1) or
                            (j < self.board_size - 1 and evaluated_pattern[i][j + 1] == 1) or
                            (i > 0 and self.board_size - 1 > j and evaluated_pattern[i - 1][j + 1] == 1)):
                        evaluated_row.append(1)
                    else:
                        if [i, j] != position:
                            evaluated_row.append(0)
                        else:
                            evaluated_row.append(1)
                evaluated_board.append(evaluated_row)
            evaluated_pattern = [row[:] for row in evaluated_board]
        return evaluated_board


if __name__ == "__main__":
    game = WaldmeisterLogic(5)
    game.field[1][1] = [0, 0]
    game.field[1][2] = [0, 0]
    game.print_board([1, 2])
    print(game.get_legal_moves_for_position([1, 2]))
