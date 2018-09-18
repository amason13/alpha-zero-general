import sys
sys.path.append('..')
from utils import *

import argparse
from keras.models import *
from keras.layers import *
from keras.optimizers import *

"""
NeuralNet for the game of TicTacToe.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloNNet by SourKream and Surag Nair.
"""
class TicTacToeNNet():
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args
        
        # Neural Net
        self.input_boards = Input(shape=(self.board_x, self.board_y))
        x = Reshape((self.board_x, self.board_y, 1))(self.input_boards)         
        x = Dense(32, activation='relu')(x)
        x = Flatten()(x)

        self.pi = Dense(self.action_size, activation='softmax', name='pi')(x)
        self.v = Dense(1, activation='tanh', name='v')(x)

        self.model = Model(inputs=self.input_boards, outputs=[self.pi, self.v])
                
        self.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=SGD(args.lr,momentum=0.9,nesterov=True))
