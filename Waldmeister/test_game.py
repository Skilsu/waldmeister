from unittest import TestCase

from WaldmeisterLogic import WaldmeisterLogic


def prepare_board():
    game = WaldmeisterLogic()
    game.field[0][6] = [0, 0]
    game.field[1][4] = [0, 0]
    game.field[2][3] = [1, 1]
    game.field[2][4] = [1, 0]
    game.field[3][2] = [1, 2]
    game.field[3][4] = [1, 2]
    game.field[4][2] = [2, 2]
    game.field[4][3] = [0, 2]
    game.field[4][4] = [2, 2]
    game.field[5][1] = [0, 1]
    game.field[5][2] = [0, 2]
    game.field[5][3] = [1, 1]
    game.field[6][1] = [1, 0]
    game.field[6][2] = [2, 0]
    return game


class TestWaldmeisterGame(TestCase):

    def test_make_move(self):
        self.fail()

    def test_reset_game(self):
        self.fail()

    def test_winner(self):
        game = prepare_board()
        if game.winner() is not None:
            self.fail()
        # TODO more test cases needed
        self.fail()

    def test_count_points(self):
        game = prepare_board()
        if game.count_points(1) == 9 and game.count_points(0) == 8:
            self.fail()
        # seems to work.. idk if something is missing.

    def test_count_points_per_layer(self):
        self.fail()

    def test_get_cleaned_boards_per_player_per_layer(self):
        self.fail()

    def test_evaluate_boards(self):
        self.fail()

    def test_evaluate_board(self):
        self.fail()

    def test__get_reward_board(self):
        self.fail()
