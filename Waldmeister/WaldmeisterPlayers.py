import numpy as np

"""
Random and Human-ineracting players for the game of Wadlmeister.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloPlayers by Surag Nair.

"""
class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanWaldmeisterPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
        moves, moves_binary = self.game.getValidMovesHuman(board, 1)

        for i in range(len(moves)):
            move = moves[i]

            if self.game.empty_board:
                print("|{}: Place Piece: {}, At: {}|".format(i, move[0], move[1]))
            else:
                print("|{}: Place Piece: {}, Move Piece: {}, From: {}, To: {}|".format(i, move[0], move[1], move[2], move[3]))

        valid_move = False
        while not valid_move:
            input_move = int(input("\nPlease enter a move number: "))

            if 0 <= input_move < len(moves):
                valid_move = True
            else:
                print("Sorry, that move is not valid. Please enter another.")

        return input_move



        """for i in range(len(valid)):
            if valid[i]:
                print(int(i/self.game.n), int(i%self.game.n))
        while True:
            # Python 3.x
            a = input()
            # Python 2.x
            # a = raw_input()

            x,y = [int(x) for x in a.split(' ')]
            a = self.game.n * x + y if x!= -1 else self.game.n ** 2
            if valid[a]:
                break
            else:
                print('Invalid')

        return a"""