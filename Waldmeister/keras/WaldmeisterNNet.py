import sys
sys.path.append('..')
from utils import *

import argparse
from keras.models import *
from keras.layers import *
from keras.optimizers import *

"""
NeuralNet for the game of Waldmeister.

Author: Abdülkerim Kilinc, github.com/AbdulkerimKilinc
Author: Nicolas Henrich, github.com/Skilsu

Date: Jan 5, 2024.

Based on the OthelloNNet by SourKream and Surag Nair.
"""


class WaldmeisterNNet():
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y, self.figures, self.player, self.height, self.color = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        # Neural Net
        input_boards11 = Input(shape=(self.board_x, self.board_y, self.figures))
        input_boards22 = Input(shape=(self.player, self.height, self.color))

        # Process first board
        x_image1 = Reshape((self.board_x, self.board_y, self.figures, 1))(input_boards11)
        h_conv1_1 = Activation('relu')(
            BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='same', use_bias=False)(x_image1)))
        h_conv2_1 = Activation('relu')(
            BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='same', use_bias=False)(h_conv1_1)))
        h_conv3_1 = Activation('relu')(
            BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='valid', use_bias=False)(h_conv2_1)))
        h_conv4_1 = Activation('relu')(
            BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='valid', use_bias=False)(h_conv3_1)))
        h_conv4_flat_1 = Flatten()(h_conv4_1)

        # Process second board
        x_image2 = Reshape((self.player, self.height, self.color, 1))(input_boards22)
        h_conv1_2 = Activation('relu')(
            BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='same', use_bias=False)(x_image2)))
        h_conv2_2 = Activation('relu')(
            BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='same', use_bias=False)(h_conv1_2)))
        h_conv3_2 = Activation('relu')(
            BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='same', use_bias=False)(h_conv2_2)))
        h_conv4_2 = Activation('relu')(
            BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='same', use_bias=False)(h_conv3_2)))
        h_conv4_flat_2 = Flatten()(h_conv4_2)

        # Concatenate the processed boards
        concatenated_features = concatenate([h_conv4_flat_1, h_conv4_flat_2])

        # Continue with the fully connected layers
        s_fc1 = Dropout(args.dropout)(
            Activation('relu')(BatchNormalization(axis=1)(Dense(1024, use_bias=False)(concatenated_features))))
        s_fc2 = Dropout(args.dropout)(Activation('relu')(BatchNormalization(axis=1)(Dense(512, use_bias=False)(s_fc1))))
        self.pi = Dense(self.action_size, activation='softmax', name='pi')(s_fc2)
        self.v = Dense(1, activation='tanh', name='v')(s_fc2)

        # Model definition and compilation
        self.model = Model(inputs=[input_boards11, input_boards22], outputs=[self.pi, self.v])
        self.model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(args.lr))
