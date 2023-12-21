"""
Board class.
Bord data:

"""


class Board():

    def __init__(self, n=8):
        self.n = n
        self.pieces = [[0 for _ in range(n)] for _ in range(n)]

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pieces[index]
