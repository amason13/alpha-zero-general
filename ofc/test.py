from OFCLogic import *
from OFCGame import *


p1 = playerHand()
p2 = playerHand()

p1.show()
p2.show()

game = OFC(p1,p2)

print(p1.is_empty())
print(p2.is_empty())
