import sys
sys.path.append('..')
from utils import *

import argparse
from keras.models import *
from keras.layers import *
from keras.optimizers import *

class SimpleNN():
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize(1)
        self.args = args

        # Neural Net
        self.input_boards = Input(shape=(self.board_x, self.board_y))
        flat_input = Flatten()(self.input_boards)
        self.hidden1 = Dense(64, activation='relu')(flat_input)
        self.hidden2 = Dense(64, activation='relu')(self.hidden1)

        self.pi = Dense(self.action_size, activation='softmax', name='pi')(self.hidden2)
        self.v = Dense(1, activation='tanh', name='v')(self.hidden2)

        self.model = Model(inputs=self.input_boards, outputs=[self.pi, self.v])
                
        self.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=SGD(args.lr,momentum=0.9,nesterov=True))
