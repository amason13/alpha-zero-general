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
        
        self.model = Sequential()
        
        self.model.add(Dense(52, input_shape=(13, 4), activation = 'relu')) # input
        
        self.model.add(Dense(64, activation='relu')) # hidden1 
        self.model.add(Dense(64, activation='relu')) # hidden2
        
        self.pi = Dense(self.action_size, activation='softmax', name='pi')
        self.v = Dense(1, activation='tanh', name='v')
        
        self.model.add([self.pi, self.v])
        
        self.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=SGD(args.lr,momentum=0.9,nesterov=True))
