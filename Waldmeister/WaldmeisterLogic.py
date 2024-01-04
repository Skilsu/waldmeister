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
        self.active_player = -1  # can be -1 or 1 to access over self.player

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.field[index]

    def print_board(self, active_position=None):
        x = -(self.board_size / 2)
        y = (self.board_size / 2) - 1
        for i in range(self.board_size * 2 - 1):
            line_str = ""
            old_x = x
            old_y = y
            for j in range(self.board_size * 2 - 1):
                x += 0.5
                y += 0.5
                if 0 <= x < self.board_size and 0 <= y < self.board_size and y == int(y) and x == int(x):
                    if active_position is not None and (x == active_position[0]
                                                        or y == active_position[1]
                                                        or active_position[1] + active_position[0] == x + y):
                        line_str = line_str + str("Nein")
                    else:
                        line_str = line_str + str(self.field[int(x)][int(y)])
                else:
                    line_str = line_str + "    "
            print(line_str)
            x = old_x + 0.5
            y = old_y - 0.5

    def make_move(self, starting_from, figure, moving_to=None, moving=None):
        # handle player position
        if self.active_player == -1:
            player = 0
        else:
            player = 1

        if moving:
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

        # change active player for next move
        if self.active_player == 1:
            self.active_player = -1
        else:
            self.active_player = 1

    def empty_board(self):
        for i in self.field:
            for j in i:
                if j is not None:
                    return False
        return True

    def get_active_positions(self, active_position):
        """
        find active positions to draw allowed lines
        """
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
        for i in self.player:
            for j in i:
                for k in j:
                    if k < self.color_amount:
                        return None
        p1 = self.count_points(0)
        p2 = self.count_points(1)
        if p1 > p2:
            return 0
        elif p2 > p1:
            return 1
        else:
            return -1

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
    game = WaldmeisterLogic()
    game.print_board()
