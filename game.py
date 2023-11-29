class Figures:
    def __init__(self, height, color):
        self.height = height
        self.color = color


class WaldmeisterGame:

    def __init__(self):
        self.player = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(2)]
        self.field = [[None for _ in range(8)] for _ in range(8)]
        self.active = None
        self.empty_board = True
        self.active_player = 0  # can be 0 or 1 to access over self.player

    def print_board(self):
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
                    if self.active and (x == self.active[0]
                                        or y == self.active[1]
                                        or self.active[1] + self.active[0] == x + y):
                        line_str = line_str + str("Nein")
                    else:
                        line_str = line_str + str(self.field[int(x)][int(y)])
                else:
                    line_str = line_str + "    "
            print(line_str)
            x = old_x + 0.5
            y = old_y - 0.5

    def make_move(self, starting_from, moving_to, figure):

        # Validate if passed figure is still available for player
        if self.player[self.active_player][figure[0]][figure[1]] >= 3:
            return

        # add figure to played figures
        self.player[self.active_player][figure[0]][figure[1]] += 1

        # change active player for next move
        if self.active_player == 1:
            self.active_player = 0
        else:
            self.active_player = 1

        # add figure to board (first round)
        if self.empty_board and game.field[starting_from[0]][starting_from[1]] is None:
            self.empty_board = False
            game.field[starting_from[0]][starting_from[1]] = figure

        # add figure to board (not first round)
        elif (game.field[moving_to[0]][moving_to[1]] is None
              and game.field[starting_from[0]][starting_from[1]] is not None):
            game.field[moving_to[0]][moving_to[1]] = game.field[starting_from[0]][starting_from[1]]
            game.field[starting_from[0]][starting_from[1]] = figure


if __name__ == "__main__":
    game = WaldmeisterGame()
    game.print_board()
    game.active = [2, 5]
    game.print_board()
