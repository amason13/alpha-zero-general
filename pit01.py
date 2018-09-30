import Arena
from MCTS import MCTS
from othello.OthelloGame import OthelloGame, display
from othello.OthelloPlayers import *
from othello.keras.CNN import NNetWrapper as CNN
from othello.keras.NN64 import NNetWrapper as NN64
from othello.keras.NN128 import NNetWrapper as N128
from othello.keras.NN256 import NNetWrapper as NN256
from othello.keras.LSTM64 import NNetWrapper as LSTM64
from othello.keras.LSTM128 import NNetWrapper as LSTM128
from othello.keras.LSTM256 import NNetWrapper as LSTM256

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

g = OthelloGame(6)

# all players
rp = RandomPlayer(g).play
gp = GreedyOthelloPlayer(g).play
hp = HumanOthelloPlayer(g).play

# nnet players
n1 = CNN(g)
n1.load_checkpoint('./othcnntemp/','best.pth.tar')
args1 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
cnn = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))


n2 = NN64(g)
n2.load_checkpoint('./othnn64temp/','best.pth.tar')
args2 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
mcts2 = MCTS(g, n2, args2)
nn64 = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

n3 = NN128(g)
n3.load_checkpoint('./othnn128temp/','best.pth.tar')
args3 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
mcts3 = MCTS(g, n3, args3)
nn128 = lambda x: np.argmax(mcts3.getActionProb(x, temp=0))

n4 = NN256(g)
n4.load_checkpoint('./othnn128temp/','best.pth.tar')
args4 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
mcts4 = MCTS(g, n4, args4)
nn256 = lambda x: np.argmax(mcts4.getActionProb(x, temp=0))

print('CNN vs NN')
arena = Arena.Arena(n1p, n2p, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('CNN vs LSTM')
arena = Arena.Arena(n1p, n3p, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('NN vs LSTM')
arena = Arena.Arena(n2p, n1p, g, display=display)
print(arena.playGames(30, verbose=False))#True))


