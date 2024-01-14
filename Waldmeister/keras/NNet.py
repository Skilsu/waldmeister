import os
import sys
import time

import numpy as np

from utils import *
from NeuralNet import NeuralNet

from .WaldmeisterNNet import WaldmeisterNNet as wnnet

sys.path.append('../..')

args = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 64,
    'cuda': True,
    'num_channels': 512,
})


class NNetWrapper(NeuralNet):
    def __init__(self, game):
        super().__init__(game)
        self.nnet = wnnet(game, args)
        self.board_x, self.board_y, self.figures, self.player, self.height, self.color = game.getBoardSize()
        self.action_size = game.getActionSize()

    def train(self, examples):
        """
        examples: list of examples, each example is of form (board, pi, v)
        """
        input_boards, target_pis, target_vs = list(zip(*examples))

        input_list_1 = [board[0] for board in input_boards]
        input_list_2 = [board[1] for board in input_boards]
        input_list_1 = np.asarray(input_list_1)
        input_list_2 = np.asarray(input_list_2)

        target_pis = np.asarray(target_pis)
        target_vs = np.asarray(target_vs)
        self.nnet.model.fit(x=[input_list_1, input_list_2], y=[target_pis, target_vs], batch_size=args.batch_size,
                            epochs=args.epochs)

    def predict(self, board):
        """
        board: np array with board
        """
        # timing
        # start = time.time()
        np_board, np_figures = board
        # preparing input
        np_board = np_board[np.newaxis, :, :]
        np_figures = np_figures[np.newaxis, :, :]

        # run
        pi, v = self.nnet.model.predict((np_board, np_figures), verbose=False)

        # print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time() - start))
        return pi[0], v[0]

    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # change extension
        filename = filename.split(".")[0] + ".h5"

        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        self.nnet.model.save_weights(filepath)

    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # change extension
        filename = filename.split(".")[0] + ".h5"

        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            e = Exception()
            e.add_note("No model in path {}".format(filepath))
            raise e

        self.nnet.model.load_weights(filepath)
