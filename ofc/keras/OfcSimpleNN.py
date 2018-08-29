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
        self.action_size = game.getActionSize()
        self.args = args

        # Neural Net
        self.input_boards = Input(shape=(13, 4))
        
        x = Dense(64, activation='relu')(x)
        x = Dense(64, activation='relu')(x)
        x = Dense(64, activation='relu')(x)

        self.pi = Dense(self.action_size, activation='softmax', name='pi')(x)
        self.v = Dense(1, activation='tanh', name='v')(x)

        self.model = Model(inputs=self.input_boards, outputs=[self.pi, self.v])
                
        self.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=SGD(args.lr,momentum=0.9,nesterov=True))
