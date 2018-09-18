import sys
sys.path.append('..')
from utils import *

import argparse
from keras.models import *
from keras.layers import *
from keras.optimizers import *

class Connect4NNet():
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        # Neural Net
        self.input_boards = Input(shape=(self.board_x, self.board_y))    # s: batch_size x board_x x board_y

        x_image = Reshape((self.board_x, self.board_y, 1))(self.input_boards)                # batch_size  x board_x x board_y x 1
        h_conv1 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='same', use_bias=False)(x_image)))         # batch_size  x board_x x board_y x num_channels
        h_conv2 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='same', use_bias=False)(h_conv1)))         # batch_size  x board_x x board_y x num_channels
        h_conv3 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='valid', use_bias=False)(h_conv2)))        # batch_size  x (board_x-2) x (board_y-2) x num_channels
        h_conv4 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(args.num_channels, 3, padding='valid', use_bias=False)(h_conv3)))        # batch_size  x (board_x-4) x (board_y-4) x num_channels
        h_conv4_flat = Flatten()(h_conv4)       
        s_fc1 = Dropout(args.dropout)(Activation('relu')(BatchNormalization(axis=1)(Dense(1024, use_bias=False)(h_conv4_flat))))  # batch_size x 1024
        s_fc2 = Dropout(args.dropout)(Activation('relu')(BatchNormalization(axis=1)(Dense(512, use_bias=False)(s_fc1))))          # batch_size x 1024
        self.pi = Dense(self.action_size, activation='softmax', name='pi')(s_fc2)   # batch_size x self.action_size
        self.v = Dense(1, activation='tanh', name='v')(s_fc2)                    # batch_size x 1

        self.model = Model(inputs=self.input_boards, outputs=[self.pi, self.v])
        self.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=Adam(args.lr))

     
class Connect4NNet2():
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        # Neural Net
        self.input_boards = Input(shape=(self.board_x, self.board_y))    # s: batch_size x board_x x board_y

        x = Dense(128, activation='relu')(self.input_boards)
        x_flat = Flatten()(x)
        
        self.pi = Dense(self.action_size, activation='softmax', name='pi')(x_flat)
        self.v = Dense(1, activation='tanh', name='v')(x_flat)

        self.model = Model(inputs=self.input_boards, outputs=[self.pi, self.v])
        self.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=Adam(args.lr))
        
        
class Connect4NNet3():
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args
        self.dim = self.board_x*self.board_y
        
        self.input_boards = Input(shape=(self.board_x, self.board_y))
        
        x_flat = Flatten()(self.input_boards)
        
        # Headline input: meant to receive sequences of 100 integers, between 1 and 10000.
        # Note that we can name any layer by passing it a "name" argument.
        self.input_sequences = Input(shape=(20, self.dim), dtype='int32')

        # This embedding layer will encode the input sequence
        # into a sequence of dense 512-dimensional vectors.
        x = Embedding(output_dim=512, input_dim=self.dim, input_length=20)(self.input_sequences)

        # A LSTM will transform the vector sequence into a single vector,
        # containing information about the entire sequence
        lstm_out = LSTM(32)(x)
        
        # Neural Net
        #self.input_boards = Input(shape=(self.board_x, self.board_y))    # s: batch_size x board_x x board_y
        #x = Dense(128, activation='relu')(self.input_boards)
        #x_flat = Flatten()(x)
        
        self.pi = Dense(self.action_size, activation='softmax', name='pi')(lstm_out)
        self.v = Dense(1, activation='tanh', name='v')(lstm_out)

        self.model = Model(inputs=self.input_sequences, outputs=[self.pi, self.v])
        self.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=Adam(args.lr))
        print(self.model.summary())
