import Arena
from MCTS import MCTS
from othello.OthelloGame import OthelloGame, display
from othello.OthelloPlayers import *
from othello.keras.NNet import NNetWrapper as NNet
from othello.keras.NNet2 import NNetWrapper as NNet2
from othello.keras.NNet3 import NNetWrapper as NNet3

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
n1 = NNet(g)
n1.load_checkpoint('./othtemp/','best.pth.tar')
args1 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))


n2 = NNet2(g)
n2.load_checkpoint('./othtemp2/','best.pth.tar')
args2 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
mcts2 = MCTS(g, n2, args2)
n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

n3 = NNet3(g)
n3.load_checkpoint('./othtemp3/','best.pth.tar')
args3 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
mcts3 = MCTS(g, n3, args3)
n3p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

arena = Arena.Arena(n2p, rp, g, display=display)
print(arena.playGames(10, verbose=False))#True))
