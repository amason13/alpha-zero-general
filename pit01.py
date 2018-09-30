import Arena
from MCTS import MCTS
from othello.OthelloGame import OthelloGame, display
from othello.OthelloPlayers import *
from othello.keras.CNN import NNetWrapper as CNN
from othello.keras.NN64 import NNetWrapper as NN64
from othello.keras.NN128 import NNetWrapper as NN128
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
n4.load_checkpoint('./othnn256temp/','best.pth.tar')
args4 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
mcts4 = MCTS(g, n4, args4)
nn256 = lambda x: np.argmax(mcts4.getActionProb(x, temp=0))

n5 = LSTM64(g)
n5.load_checkpoint('./othlstm64temp/','best.pth.tar')
args5 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
mcts5 = MCTS(g, n5, args5)
lstm64 = lambda x: np.argmax(mcts5.getActionProb(x, temp=0))

n6 = LSTM128(g)
n6.load_checkpoint('./othlstm128temp/','best.pth.tar')
args6 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
mcts6 = MCTS(g, n6, args6)
lstm128 = lambda x: np.argmax(mcts6.getActionProb(x, temp=0))

n7 = LSTM256(g)
n7.load_checkpoint('./othlstm256temp/','best.pth.tar')
args7 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
mcts7 = MCTS(g, n7, args7)
lstm256 = lambda x: np.argmax(mcts7.getActionProb(x, temp=0))


print('CNN vs NN64')
arena = Arena.Arena(cnn, nn64, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('CNN vs NN128')
arena = Arena.Arena(cnn, nn128, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('cnn vs nn256')
arena = Arena.Arena(cnn, nn256, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('CNN vs lstm64')
arena = Arena.Arena(cnn, lstm64, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('CNN vs lstm128')
arena = Arena.Arena(cnn, lstm128, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('cnn vs lstm256')
arena = Arena.Arena(cnn, lstm256, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('nn64 vs nn128')
arena = Arena.Arena(nn64, nn128, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('nn64 vs nn256')
arena = Arena.Arena(nn64, nn256, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('nn64 vs lstm64')
arena = Arena.Arena(nn64, lstm64, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('nn64 vs lstm128')
arena = Arena.Arena(nn64, lstm128, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('nn64 vs lstm256')
arena = Arena.Arena(nn64, lstm256, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('nn128 vs nn256')
arena = Arena.Arena(nn128, nn256, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('nn128 vs lstm64')
arena = Arena.Arena(nn128, lstm64, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('nn128 vs lstm128')
arena = Arena.Arena(nn128, lstm128, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('nn128 vs lstm256')
arena = Arena.Arena(nn128, lstm256, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('nn256 vs lstm64')
arena = Arena.Arena(nn256, lstm64, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('nn256 vs lstm128')
arena = Arena.Arena(nn256, lstm128, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('nn256 vs lstm256')
arena = Arena.Arena(nn256, lstm256, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('lstm64 vs lstm128')
arena = Arena.Arena(lstm64, lstm128, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('lstm64 vs lstm256')
arena = Arena.Arena(lstm64, lstm256, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('lstm128 vs lstm256')
arena = Arena.Arena(lstm128, lstm256, g, display=display)
print(arena.playGames(30, verbose=False))#True))
