# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
import numpy as np
import itertools
from ofc import methods
from treys import Deck

"""
Game class implementation for the game of Open Faced Chinese Poker.
Author: amason13
Date: 23 Aug, 2018.
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
        
        
    def opponent_hand(self, player):
        
        # map 1 or -1 to playerHand object
        player_hand = self.PLAYERS_HAND_DICT[player]
        
        # return opponent's playerHand object
        if player_hand == self.ph1:
            return self.ph2
        elif player_hand == self.ph2:
            return self.ph1
        else:
            print('Player Error')

    def getInitBoard(self):
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
            self.ph2.dealt_cards=self.deck.draw(13)
            self.ph2.set_fantasy()
            
        # get initial board for each deal - (represented by a 52x1 numpy array) 
        board = methods.hands_to_board(self.ph1,self.ph2)
        return board

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        # board array always same size
        return (52,1)

    def getActionSize(self,player):
        """
        Returns:
            actionSize: number of all possible actions
        """
        # maps 1 or -1 to playerHand object
        player_hand = self.PLAYERS_HAND_DICT[player]
        
        # if the first round where 5 cards are dealt and must be placed (assuming not in fantasy)
        if len(player_hand.dealt_cards) == 5:
            return 232
        else: # for self.n = 1 the regular variant - more logic needs to be added here for n=2,3..
            return np.count_nonzero(player_hand.get_available_actions()==1) 

            
    def getNextState(self, board, player, action):
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
        
        # if in fantasy
        if player_hand.in_fantasy == 1:
            pass
        else:
        
            board = np.array(board)
            T = player_hand.top_hand
            M = player_hand.middle_hand
            B = player_hand.bottom_hand
            D = player_hand.discards
            
            
            # dictionaries mapping index labels of valid move vectors, to the combination of hands where card in playerHand.dealt_cards should be allocated
            ACTION_DICT_1 = {0:T, 1:M, 2:B}
            
            ACTION_DICT_2 = {0:(T,T),1:(T,M),2:(T,B),3:(M,T),4:(M,M),5:(M,B),6:(B,T),7:(B,M),8:(B,B)}
           
            ACTION_DICT_3 = {0:(T,T,D),1:(T,D,T),2:(D,T,T),
                             3:(T,M,D),4:(T,D,M),5:(D,T,M),
                             6:(T,B,D),7:(T,D,B),8:(D,T,B),
                             9:(M,T,D),10:(M,D,T),11:(D,M,T),
                             12:(M,M,D),13:(M,D,M),14:(D,M,M),
                             15:(M,B,D),16:(M,D,B),17:(D,M,B),
                             18:(B,T,D),19:(B,D,T),20:(D,B,T),
                             21:(B,M,D),22:(B,D,M),23:(D,B,M),
                             24:(B,B,D),25:(B,D,B),26:(D,B,B)}
            
            five_card_combos = [(T, T, T, M, M),(T, T, T, M, B),(T, T, T, B, M),(T, T, T, B, B),(T, T, M, T, M),(T, T, M, T, B),(T, T, M, M, T),(T, T, M, M, M),
                                (T, T, M, M, B),(T, T, M, B, T),(T, T, M, B, M),(T, T, M, B, B),(T, T, B, T, M),(T, T, B, T, B),(T, T, B, M, T),(T, T, B, M, M),(T, T, B, M, B),(T, T, B, B, T),(T, T, B, B, M),(T, T, B, B, B),(T, M, T, T, M),(T, M, T, T, B),(T, M, T, M, T),(T, M, T, M, M),
                                (T, M, T, M, B),(T, M, T, B, T),(T, M, T, B, M),(T, M, T, B, B),(T, M, M, T, T),(T, M, M, T, M),(T, M, M, T, B),(T, M, M, M, T),(T, M, M, M, M),(T, M, M, M, B),(T, M, M, B, T),(T, M, M, B, M),(T, M, M, B, B),(T, M, B, T, T),(T, M, B, T, M),(T, M, B, T, B),
                                (T, M, B, M, T),(T, M, B, M, M),(T, M, B, M, B),(T, M, B, B, T),(T, M, B, B, M),(T, M, B, B, B),(T, B, T, T, M),(T, B, T, T, B),(T, B, T, M, T),(T, B, T, M, M),(T, B, T, M, B),(T, B, T, B, T),(T, B, T, B, M),(T, B, T, B, B),(T, B, M, T, T),(T, B, M, T, M),
                                (T, B, M, T, B),(T, B, M, M, T),(T, B, M, M, M),(T, B, M, M, B),(T, B, M, B, T),(T, B, M, B, M),(T, B, M, B, B),(T, B, B, T, T),(T, B, B, T, M),(T, B, B, T, B),(T, B, B, M, T),(T, B, B, M, M),(T, B, B, M, B),(T, B, B, B, T),(T, B, B, B, M),(T, B, B, B, B),
                                (M, T, T, T, M),(M, T, T, T, B),(M, T, T, M, T),(M, T, T, M, M),(M, T, T, M, B),(M, T, T, B, T),(M, T, T, B, M),(M, T, T, B, B),(M, T, M, T, T),(M, T, M, T, M),(M, T, M, T, B),(M, T, M, M, T),(M, T, M, M, M),(M, T, M, M, B),(M, T, M, B, T),(M, T, M, B, M),
                                (M, T, M, B, B),(M, T, B, T, T),(M, T, B, T, M),(M, T, B, T, B),(M, T, B, M, T),(M, T, B, M, M),(M, T, B, M, B),(M, T, B, B, T),(M, T, B, B, M),(M, T, B, B, B),(M, M, T, T, T),(M, M, T, T, M),(M, M, T, T, B),(M, M, T, M, T),(M, M, T, M, M),(M, M, T, M, B),
                                (M, M, T, B, T),(M, M, T, B, M),(M, M, T, B, B),(M, M, M, T, T),(M, M, M, T, M),(M, M, M, T, B),(M, M, M, M, T),(M, M, M, M, M),(M, M, M, M, B),(M, M, M, B, T),(M, M, M, B, M),(M, M, M, B, B),(M, M, B, T, T),(M, M, B, T, M),(M, M, B, T, B),(M, M, B, M, T),
                                (M, M, B, M, M),(M, M, B, M, B),(M, M, B, B, T),(M, M, B, B, M),(M, M, B, B, B),(M, B, T, T, T),(M, B, T, T, M),(M, B, T, T, B),(M, B, T, M, T),(M, B, T, M, M),(M, B, T, M, B),(M, B, T, B, T),(M, B, T, B, M),(M, B, T, B, B),(M, B, M, T, T),(M, B, M, T, M),
                                (M, B, M, T, B),(M, B, M, M, T),(M, B, M, M, M),(M, B, M, M, B),(M, B, M, B, T),(M, B, M, B, M),(M, B, M, B, B),(M, B, B, T, T),(M, B, B, T, M),(M, B, B, T, B),(M, B, B, M, T),(M, B, B, M, M),(M, B, B, M, B),(M, B, B, B, T),(M, B, B, B, M),(M, B, B, B, B),
                                (B, T, T, T, M),(B, T, T, T, B),(B, T, T, M, T),(B, T, T, M, M),(B, T, T, M, B),(B, T, T, B, T),(B, T, T, B, M),(B, T, T, B, B),(B, T, M, T, T),(B, T, M, T, M),(B, T, M, T, B),(B, T, M, M, T),(B, T, M, M, M),(B, T, M, M, B),(B, T, M, B, T),(B, T, M, B, M),
                                (B, T, M, B, B),(B, T, B, T, T),(B, T, B, T, M),(B, T, B, T, B),(B, T, B, M, T),(B, T, B, M, M),(B, T, B, M, B),(B, T, B, B, T),(B, T, B, B, M),(B, T, B, B, B),(B, M, T, T, T),(B, M, T, T, M),(B, M, T, T, B),(B, M, T, M, T),(B, M, T, M, M),(B, M, T, M, B),
                                (B, M, T, B, T),(B, M, T, B, M),(B, M, T, B, B),(B, M, M, T, T),(B, M, M, T, M),(B, M, M, T, B),(B, M, M, M, T),(B, M, M, M, M),(B, M, M, M, B),(B, M, M, B, T),(B, M, M, B, M),(B, M, M, B, B),(B, M, B, T, T),(B, M, B, T, M),(B, M, B, T, B),(B, M, B, M, T),
                                (B, M, B, M, M),(B, M, B, M, B),(B, M, B, B, T),(B, M, B, B, M),(B, M, B, B, B),(B, B, T, T, T),(B, B, T, T, M),(B, B, T, T, B),(B, B, T, M, T),(B, B, T, M, M),(B, B, T, M, B),(B, B, T, B, T),(B, B, T, B, M),(B, B, T, B, B),(B, B, M, T, T),(B, B, M, T, M),
                                (B, B, M, T, B),(B, B, M, M, T),(B, B, M, M, M),(B, B, M, M, B),(B, B, M, B, T),(B, B, M, B, M),(B, B, M, B, B),(B, B, B, T, T),(B, B, B, T, M),(B, B, B, T, B),(B, B, B, M, T),(B, B, B, M, M),(B, B, B, M, B),(B, B, B, B, T),(B, B, B, B, M),(B, B, B, B, B)]
            ACTION_DICT_5 = dict(zip(range(232),five_card_combos))
            
            CARDS_DEALT_TO_DICT_MAP = {1:ACTION_DICT_1,2:ACTION_DICT_2,3:ACTION_DICT_3,5:ACTION_DICT_5}
        
            # allocate cards to hands
            if len(player_hand.dealt_cards) == 1:
                ACTION_DICT_1[action].append(player_hand.dealt_cards.pop(0))
            else: 
                for i in range(len(player_hand.dealt_cards)):
                    CARDS_DEALT_TO_DICT_MAP[len(player_hand.dealt_cards)][action].append(player_hand.dealt_cards.pop(0))
        
            # draw the next n cards for the next round
            player_hand.dealt_cards=self.deck.draw(self.n)
        
        # determine next board
        nextboard = methods.players_to_board(self.opponent(player),player)
        return (nextboard, self.opponent(player))
        
        

     
        
    def getValidMoves(self, board, player):
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
        player_hand = self.PLAYERS_HAND_DICT[player]
        
        # convert board to player hands
        methods.board_to_hands(player_hand,self.opponent_hand(player_hand))
        
        # get available actions
        return player_hand.get_available_actions()
    

    def getGameEnded(self, board, player):
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
            score = methods.score_hands(player_hand,self.opponent_hand(player_hand))
            
            # get player hands ready for next hand - updating fantasy variable
            player_hand.next_hand()
            op_hand.next_hand()
            # shuffle all the cards back into the deck
            self.deck.shuffle()
            
            return score
        else:
            return False

        
    def getCanonicalForm(self, board, player):
        
        # maps 1 or -1 to playerHand object
        player_hand = self.PLAYERS_HAND_DICT[player]
        # canonical form of board is not as simple as *-1 like in other games, 
        # due to discards which can only be seen by current player.
        can_board = methods.hands_to_board(player_hand,self.opponent_hand(player_hand))
        return can_board
    
    
    def getSymmetries(self, board, pi):
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
        # tuple with policy
        for el in l:
            el = (el,pi)
        
        return l

    def stringRepresentation(self, board):
        return board.tostring()

    def display(self,player_hand):
        print('PLAYER1:')
        player_hand.show()
        print('PLAYER2:')
        self.opponent_hand(player_hand).show()
