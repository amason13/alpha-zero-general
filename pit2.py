import Arena
from MCTS import MCTS
from connect4.Connect4Game import Connect4Game, display
from connect4.Connect4Players import *
from connect4.keras.CNN import NNetWrapper as NNet
from connect4.keras.NN128 import NNetWrapper as NNet2
from connect4.keras.LSTM128 import NNetWrapper as NNet3

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

g = Connect4Game()

# all players
#rp = RandomPlayer(g).play
#gp = GreedyOthelloPlayer(g).play
#hp = HumanOthelloPlayer(g).play

# nnet players
n1 = NNet(g)
n1.load_checkpoint('./con4temp/','best.pth.tar')
args1 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))


n2 = NNet2(g)
n2.load_checkpoint('./con4temp2/','best.pth.tar')
args2 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
mcts2 = MCTS(g, n2, args2)
n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

n3 = NNet3(g)
n3.load_checkpoint('./con4temp3/','best.pth.tar')
args3 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
mcts3 = MCTS(g, n3, args3)
n3p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

print('CNN vs NN')
arena = Arena.Arena(n1p, n2p, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('CNN vs LSTM')
arena = Arena.Arena(n1p, n3p, g, display=display)
print(arena.playGames(30, verbose=False))#True))

print('NN vs LSTM')
arena = Arena.Arena(n2p, n1p, g, display=display)
print(arena.playGames(30, verbose=False))#True))


