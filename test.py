from Game import Game
import numpy as np
import itertools
from .OFCLogic import *
from treys import Deck
from copy import deepcopy
from .OFCGame import *


p1 = playerHand()
p2 = playerHand()

p1.show()
p2.show()

game = OFC(p1,p2)

print(p1.is_empty())
print(p2.is_empty())
