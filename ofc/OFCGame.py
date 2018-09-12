from Game import Game
import numpy as np
import itertools
from .OFCLogic import *
from treys import Deck
from copy import deepcopy

"""
Game class implementation for the game of Open Faced Chinese Poker.
Author: amason13
Date: 29 Aug, 2018.
"""
class OFC(Game):
    # ph1, ph2 are playerHand objects, n = 1,2,3 for different variants of ofc.
    def __init__(self,ph1,ph2,n=1):
        # initiate playerHand obvjects
        self.ph1 = ph1
        self.ph2 = ph2
        # initiate deck
        self.deck = Deck()
        self.n = n
        # dictionary which maps player (1 or -1) so it's playerHand object
        self.PLAYERS_HAND_DICT = {1:self.ph1,-1:self.ph2}
        
        
        
    def opponent_hand(self, player_hand):
        # return opponent's playerHand object
        if player_hand == self.ph1:
            return self.ph2
        elif player_hand == self.ph2:
            return self.ph1
        else:
            print('Player Error')

    def getInitBoard(self):
        print('getinitboard')
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        # deal initial cards to each player - 5 if not in fantasy, 13 and set hand if in fantasy land.
        if self.ph1.in_fantasy == 0:
            self.ph1.dealt_cards=self.deck.draw(5)
        else: 
            self.ph1.dealt_cards=self.deck.draw(13)
            self.ph1.set_fantasy()
            
        if self.ph2.in_fantasy == 0:
            self.ph2.dealt_cards=self.deck.draw(5)
        else:
        #if self.ph2.in_fantasy == 1:
            self.ph2.dealt_cards=self.deck.draw(13)
            self.ph2.set_fantasy()
            
        # get initial board for each deal - (represented by a 52x1 numpy array) 
        board = hands_to_board(self.ph1,self.ph2)
        print(board)
        return board
        

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        # board array always same size
        return (4,13)

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        return 235
            
    def getNextState(self, board, player, action):
        print('nextstate')
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player - integer corresponding to a given action in dictionary
        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        # maps 1 or -1 to playerHand object
        player_hand = self.PLAYERS_HAND_DICT[player]
        op_hand = self.PLAYERS_HAND_DICT[-1*player]
        # copy players hands
        #dummy_player_hand = deepcopy(player_hand)
        #dummy_op_hand = deepcopy(op_hand)
        # copy and reshuffle deck
        #dummy_deck = deepcopy(self.deck)
        #dummy_deck.reshuffle()
        player_hand.execute_move(action)
        player_hand.dealt_cards = []
        if op_hand.is_empty == 1:
            print('op empty')
            op_hand.dealt_cards.append(self.deck.draw(5))
        else:
            op_hand.dealt_cards.append(self.deck.draw(self.n))
        # determine next board
        nextboard = hands_to_board(player_hand,op_hand)
        
        return nextboard, -1*player
        
        
    def getValidMoves(self, board, player):
        print('getvalidmoves',player)
        """
        Input:
            board: current board
            player: current player
        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        # map 1 or -1 to player hand
        player_hand = deepcopy(self.PLAYERS_HAND_DICT[player])
        opponent_hand = deepcopy(self.PLAYERS_HAND_DICT[-player])
        # convert board to player hands
        board_to_hands(board,player_hand,opponent_hand)
        
        # get available actions
        valid_moves=player_hand.get_available_actions()
        return valid_moves
    

    def getGameEnded(self, board, player):
        print('getgameended')
        """
        Input:
            board: current board
            player: current player (1 or -1)
        Returns:
            r: False if game has not ended. 
               Score if game has ended (could be 0).
               
        """
        player_hand = self.PLAYERS_HAND_DICT[player]
        op_hand = self.opponent_hand(player_hand)
        
        # if players hand and opponents hands are full, score player, else return False
        if (player_hand.is_full==1) and (op_hand.is_full==1):
            score = score_hands(player_hand,self.opponent_hand(player_hand))
            
            # get player hands ready for next hand - updating fantasy variable
            player_hand.next_hand()
            op_hand.next_hand()
            # shuffle all the cards back into the deck
            self.deck.shuffle()

            print('game ended')
            return score
        else:
            return False

        
    def getCanonicalForm(self, board, player):
        print(board)
        
        player_hand = self.PLAYERS_HAND_DICT[player]
        op_hand = self.PLAYERS_HAND_DICT[-player]
        
        can_board = hands_to_board(player_hand,op_hand)
        print(can_board)
        return can_board
    
    
    def getSymmetries(self, board, pi):
        print('getsymm')
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()
        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        # Symmetries in this context only occur by mapping suits to other suits. 
        # For example the state [Ah Kh Qh Jh Ts] is the same as [Ad Kd Qd Jd Tc].
        board = board.reshape(1,52)
        board = board[0]
        # separate into suits            
        S = [board[i] for i in range(0,13)]
        H = [board[i] for i in range(13,26)]
        D = [board[i] for i in range(26,39)]
        C = [board[i] for i in range(39,52)]
        
        # create a list of all permutations of the suits
        l=[]
        for elem in itertools.permutations([S,H,D,C],4):
            l.append(elem)
            
        # transfor each permutation element in the list to a deck of cards, 
        # reordered according to some permutation of the suits.
        for i in range(len(l)):
            l[i] = l[i][0]+l[i][1]+l[i][2]+l[i][3]
            
        # for each deck, assign each card after permutation to its position on the original board to get symmetries
        for deck in l:
            for i in range(52):
                deck[i]=board[i]
            deck = np.array(deck)
            #deck = deck[np.newaxis,:]

        # tuple with policy
        l = [(el,pi) for el in l]
        
        return l 

    def stringRepresentation(self, board):
        return board.tostring()

    def display(self, player):
        # maps 1 or -1 to playerHand object
        player_hand = self.PLAYERS_HAND_DICT[player]
        
        print('Player: ', player)
        player_hand.show()
        
        print('Player: ', -player)
        self.opponent_hand(player_hand).show()

        
p1 = playerHand()
p2 = playerHand()

p1.show()
p2.show()

game = OFC(p1,p2)

print(p1.is_empty())
print(p2.is_empty())
