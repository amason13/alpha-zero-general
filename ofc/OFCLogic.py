from treys import Card, Evaluator
import itertools
import numpy as np
from copy import deepcopy

evaluator = Evaluator()

class playerHand:
    
    def __init__(self):
        
        self.dealt_cards = []
        self.top_hand = []
        self.middle_hand = []
        self.bottom_hand = []
        self.discards = []
        self.in_fantasy = 0
        
    def reset(self):
        self.__init__()
        
    def next_hand(self):
        if self.qualifies_fantasy()==1:
            self.reset()
            self.in_fantasy = 1
        else:
            self.reset()
        
    def is_misset(self):
        # bypass incomplete hands
        if (len(self.top_hand)<3) or (len(self.middle_hand)<5) or (len(self.bottom_hand)<5):
            return 0
        
        t = evaluator.evaluate(self.top_hand,[])
        m = evaluator.evaluate(self.middle_hand,[])
        b = evaluator.evaluate(self.bottom_hand,[])
        
        if not t >= m >= b:
            return 1
        else:
            return 0


    
    def qualifies_fantasy(self):
        # if previously not in fantasy land
        if self.prev_fantasy==0:
            # bypass incomplete hands
            if (len(self.top_hand)<3) or (len(self.middle_hand)<5) or (len(self.bottom_hand)<5):
                return 0
            
            if self.is_misset == 1:    
                return 0
            else:
                if top_royalties(self.top_hand) > 6:
                    return 1  
                
        # if previously in fantasy land        
        else:    
            mid_rank = evaluator.evaluate(self.middle_hand,[])
            bot_rank = evaluator.evaluate(self.bottom_hand,[])
            
            mid = evaluator.get_rank_class(mid_rank)
            bot = evaluator.get_rank_class(bot_rank)
            
            BOTTOM_RANK_TO_ROYALTY = {
                1: 15, # Straight flush
                2: 10, # Quads
                3: 6,  # Full house
                4: 4,  # Flush
                5: 2,  # Straight
                6: 0,  # Trips
                7: 0,  # 2 pair
                8: 0,  # Pair
                9: 0   # high card
            }
            
            MIDDLE_RANK_TO_ROYALTY = {
                1: 30, # Straight flush
                2: 20, # Quads
                3: 12, # Full house
                4: 8,  # Flush
                5: 4,  # Straight
                6: 2,  # Trips
                7: 0,  # 2 pair
                8: 0,  # Pair
                9: 0   # high card
            }
            
            if (top_royalties(self.top_hand)>9) or (MIDDLE_RANK_TO_ROYALTY[mid]>9) or (BOTTOM_RANK_TO_ROYALTY[bot]>9):
                return 1
            else:
                return 0
        
        
    def get_royalties(self):
    
        top_rank = evaluator.evaluate(self.top_hand,[])
        mid_rank = evaluator.evaluate(self.middle_hand,[])
        bot_rank = evaluator.evaluate(self.bottom_hand,[])
        
        mid = evaluator.get_rank_class(mid_rank)
        bot = evaluator.get_rank_class(bot_rank)
        
        royalties = 0
        
        BOTTOM_RANK_TO_ROYALTY = {
            1: 15, # Straight flush
            2: 10, # Quads
            3: 6,  # Full house
            4: 4,  # Flush
            5: 2,  # Straight
            6: 0,  # Trips
            7: 0,  # 2 pair
            8: 0,  # Pair
            9: 0   # high card
        }
        
        MIDDLE_RANK_TO_ROYALTY = {
            1: 30, # Straight flush
            2: 20, # Quads
            3: 12, # Full house
            4: 8,  # Flush
            5: 4,  # Straight
            6: 2,  # Trips
            7: 0,  # 2 pair
            8: 0,  # Pair
            9: 0   # high card
        }
        
        # need to add royal flushes into here too
        if not bot_rank<=mid_rank<=top_rank: 
            royalties = 0
        elif mid_rank == 1:
            royalties += 75 + top_royalties(self.top_hand)
        elif bot_rank ==1:
            royalties += 50 +MIDDLE_RANK_TO_ROYALTY[mid] + top_royalties(self.top_hand)
        else:
            royalties += MIDDLE_RANK_TO_ROYALTY[mid] + BOTTOM_RANK_TO_ROYALTY[bot] + top_royalties(self.top_hand)
       
        return royalties
        



    def set_fantasy(self):
        
        min_tot_rank = 0
        max_royalties = 0
        best_top = []
        best_mid = []
        best_bot = []
        
        bottomcombos = itertools.combinations(self.dealt_cards, 5)
          
        for bcombo in bottomcombos:
            
            remaining_cards = list(set(self.dealt_cards)-set(bcombo))
            middlecombos = itertools.combinations(remaining_cards,5)
            
            for mcombo in middlecombos:
                
                remaining_cards_2 = list(set(remaining_cards)-set(mcombo))
                topcombos = itertools.combinations(remaining_cards_2,3)
                
                
                for tcombo in topcombos:
                    
                    discard = list(set(remaining_cards_2)-set(tcombo))
                    
                    self.top_hand = tcombo
                    self.middle_hand = mcombo
                    self.bottom_hand = bcombo
                    self.discards = discard
                    
                    trank = evaluator.evaluate(self.top_hand,[])
                    mrank = evaluator.evaluate(self.middle_hand,[])
                    brank = evaluator.evaluate(self.bottom_hand,[])
                    
                    totrank = trank + mrank + brank
                    royalties = self.get_royalties()
                    
                    if royalties>max_royalties:
                        
                        max_royalties = royalties
                        best_top = self.top_hand
                        best_mid = self.middle_hand
                        best_bot = self.bottom_hand
                        discard = self.discards
                        min_tot_rank = totrank
                        
                    elif (royalties == max_royalties) and (royalties>0):
                        if totrank < min_tot_rank:
                            max_royalties = royalties
                            best_top = self.top_hand
                            best_mid = self.middle_hand
                            best_bot = self.bottom_hand
                            discard = self.discards
                            min_tot_rank = totrank
                        
                        
        self.top_hand = best_top
        self.middle_hand = best_mid
        self.bottom_hand = best_bot
        self.discards = discard
        self.dealt_cards =  []

    
    
    def show(self):
        print("Top:")
        print(Card.print_pretty_cards(self.top_hand))
        print("Middle:")
        print(Card.print_pretty_cards(self.middle_hand))
        print("Bottom:")
        print(Card.print_pretty_cards(self.bottom_hand))


    def get_available_actions(self):
        T=self.top_hand
        M=self.middle_hand
        B=self.bottom_hand
            
        if len(self.dealt_cards)==5:
            
            return np.ones(232)
        
        elif len(self.dealt_cards)==3:
            pass # need to add the logic for pinapple here
        
        elif len(self.dealt_cards)==2:
            pass # need to add the logic for 2 card draw version
    
        else:
            t,m,b = 0,0,0
            
            if len(T)<3:
                t = 1
            
            if len(M)<5:
                m = 1
                
            if len(B)<5:
                b = 1     
            
        return np.array([t,m,b]) 
   
    def is_empty(self):
        
        if not (self.top_hand==[]) and (self.middle_hand==[]) and (self.bottom_hand==[]) and (self.discards==[]):
            return 0
        else:
            return 1

    def is_full(self):
        
        if not (len(self.top_hand)==3) and (len(self.middle_hand)==5) and (len(self.bottom_hand)==5) and (len(self.discards)==3):
            return 0
        else:
            return 1
        
        
        
    def score(self, opponent):
    
        top_rank1 = evaluator.evaluate(self.top_hand,[])
        mid_rank1 = evaluator.evaluate(self.middle_hand,[])
        bot_rank1 = evaluator.evaluate(self.bottom_hand,[])
        
        top_rank2 = evaluator.evaluate(opponent.top_hand,[])
        mid_rank2 = evaluator.evaluate(opponent.middle_hand,[])
        bot_rank2 = evaluator.evaluate(opponent.bottom_hand,[])
        
        # if both players foul
        if (not bot_rank1<=mid_rank1<top_rank1) and (not bot_rank2<=mid_rank2<=top_rank2):
            return (0,0)
            
        # if player 1 only fouls
        elif not bot_rank1<=mid_rank1<=top_rank1:
            r = opponent.get_royalties()
            return (-6-r,6+r)
        
        # if player 2 only fouls
        elif not bot_rank2<=mid_rank2<=top_rank2:
            r = self.get_royalties()
            return (6+r,-6-r)
        
        # if neither player fouls    
        else:
            r1 = self.get_royalties()
            r2 = opponent.get_royalties()
            
            # bottom hand
            if bot_rank1<bot_rank2:
                bs = 1
            elif bot_rank1 == bot_rank2:
                bs = 0
            else: bs = -1
            # middle hand
            if mid_rank1<mid_rank2:
                ms = 1
            elif mid_rank1 == mid_rank2:
                ms = 0
            else: ms = -1
            # top hand
            if top_rank1<top_rank2:
                ts = 1
            elif top_rank1>top_rank2:
                ts = -1
                
            # the folowing should take care of the 3-to-5 card mapping being many-to-one
            else:
                dummy_top1 = [self.top_hand[0],self.top_hand[1],self.top_hand[2]]
                dummy_top2 = [opponent.top_hand[0],opponent.top_hand[1],opponent.top_hand[2]]
                ranked1 = split_by_rank(dummy_top1)
                ranked2 = split_by_rank(dummy_top2)
                
                if len(ranked1[0]) == 2: # for pairs
                    if Card.get_rank_int(ranked1[1][0]) == Card.get_rank_int(ranked2[1][0]):
                        ts = 0
                    elif Card.get_rank_int(ranked1[1][0]) > Card.get_rank_int(ranked2[1][0]):
                        ts = 1
                    else:
                        ts = -1
                        
                else:   # for high cards
                    if Card.get_rank_int(ranked1[0][0]) > Card.get_rank_int(ranked2[0][0]):
                        ts = 1
                    elif Card.get_rank_int(ranked1[0][0]) < Card.get_rank_int(ranked2[0][0]):
                        ts = -1
                    else:
                        if Card.get_rank_int(ranked1[1][0]) > Card.get_rank_int(ranked2[1][0]):
                            ts = 1
                        elif Card.get_rank_int(ranked1[1][0]) < Card.get_rank_int(ranked2[1][0]):
                            ts = -1
                        else:
                            if Card.get_rank_int(ranked1[2][0]) > Card.get_rank_int(ranked2[2][0]):
                                ts = 1
                            elif Card.get_rank_int(ranked1[2][0]) < Card.get_rank_int(ranked2[2][0]):
                                ts = -1
                            else:
                                ts = 0
                    
            
            # calculate sum of individual score
            s = bs + ms + ts
            
            # double score if player wins all three hands (as per OFC scoring rules)
            if s % 3 == 0:
                s = 2*s
            
            # calculate player1 score by adding difference of royalties
            s = s + r1 - r2
            
            return s
        
    def hands_to_board(self,opponent):
    
        full_deck = []
    
        for suit, val in Card.CHAR_SUIT_TO_INT_SUIT.items():
            for rank in Card.STR_RANKS:
                        full_deck.append(Card.new(rank + suit))
        
        board = np.zeros(52)
        
        for card in self.top_hand:
            board[full_deck.index(card)] = 1
            
        for card in self.middle_hand:
            board[full_deck.index(card)] = 2
            
        for card in self.bottom_hand:
            board[full_deck.index(card)] = 3
    
        for card in self.discards:
            board[full_deck.index(card)] = 4
            
        for card in self.dealt_cards:
            board[full_deck.index(card)] = 5
        
        for card in opponent.top_hand:
            board[full_deck.index(card)] = -1
            
        for card in opponent.middle_hand:
            board[full_deck.index(card)] = -2
            
        for card in opponent.bottom_hand:
            board[full_deck.index(card)] = -3
    
        return np.array(board)

def split_by_rank(cards):
    
    aces = []
    kings = []
    queens = []
    jacks = []
    tens = []
    nines = []
    eights = []
    sevens = []
    sixes = []
    fives = []
    fours = []
    threes = []
    twos = []
    
    for card in cards:
        if Card.get_rank_int(card)==0:
            twos.append(card)
        elif Card.get_rank_int(card)==1:
            threes.append(card)
        elif Card.get_rank_int(card)==2:
            fours.append(card)
        elif Card.get_rank_int(card)==3:
            fives.append(card)
        elif Card.get_rank_int(card)==4:
            sixes.append(card)
        elif Card.get_rank_int(card)==5:
            sevens.append(card)
        elif Card.get_rank_int(card)==6:
            eights.append(card)
        elif Card.get_rank_int(card)==7:
            nines.append(card)
        elif Card.get_rank_int(card)==8:
            tens.append(card)
        elif Card.get_rank_int(card)==9:
            jacks.append(card)
        elif Card.get_rank_int(card)==10:
            queens.append(card)
        elif Card.get_rank_int(card)==11:
            kings.append(card)
        elif Card.get_rank_int(card)==12:
            aces.append(card)
        else:
            return 'Card rank ERROR'
        
    all_ranks = [aces,kings,queens,jacks,tens,nines,eights,sevens,sixes,fives,fours,threes,twos]
    
    rank_split = []
    
    for rank in all_ranks:
        if len(rank)>0:
            rank_split.append(rank)
    
    rank_split.sort(key=len, reverse=True)
    
    return rank_split
        
def split_by_suit(cards):
    
    spades = []
    hearts = []
    diamonds = []
    clubs = []
    
    for card in cards:
        if Card.get_suit_int(card)==1:
            spades.append(card)
        elif Card.get_suit_int(card)==2:
            hearts.append(card)
        elif Card.get_suit_int(card)==4:
            diamonds.append(card)
        elif Card.get_suit_int(card)==8:
            clubs.append(card)
        else:
            return 'Card suit ERROR'
        
    all_suits = [spades,hearts,diamonds,clubs]
    
    suit_split = []
    for suit in all_suits:
        if len(suit)>0:
            suit_split.append(suit)
    
    suit_split.sort(key=len, reverse=True)
    
    return suit_split

    
def get_max_rank(cards):
    max_rank = 0
    for c in cards:
        if Card.get_rank_int(c)>max_rank:
            max_rank=Card.get_rank_int(c)
    return max_rank


def get_min_rank(cards):
    min_rank = 0
    for c in cards:
        if Card.get_rank_int(c)<min_rank:
            min_rank=Card.get_rank_int(c)
    return min_rank
        

def top_royalties(cards):
    ranked_cards = split_by_rank(cards)
    top_roy=0
    if len(ranked_cards) == 1:
        top_roy += Card.get_rank_int(ranked_cards[0][0])+10
    elif len(ranked_cards) == 2:
        top_roy += Card.get_rank_int(ranked_cards[0][0])-3
    return top_roy
    
def try_remove(myelement, mylist):
    if myelement in mylist:
        mylist.remove(myelement)

def estimate_score(hand1, hand2, deck):
    # number of iterations
    n=10000
    
    score = 0


    for i in range(n):
        # make a copy of the remaining deck and shuffle
        dummy = deepcopy(deck)
        dummy.reshuffle()
        
        # make a copy of each player
        dummyp1 = deepcopy(hand1)
        dummyp2 = deepcopy(hand2)
        
        # randomly fill up hands
        while len(dummyp1.top_hand)<3:
            dummyp1.top_hand.append(dummy.draw(1))
        while len(dummyp1.middle_hand)<5:
            dummyp1.middle_hand.append(dummy.draw(1))
        while len(dummyp1.bottom_hand)<5:
            dummyp1.bottom_hand.append(dummy.draw(1))
               
        while len(dummyp2.top_hand)<3:
            dummyp2.top_hand.append(dummy.draw(1))
        while len(dummyp2.middle_hand)<5:
            dummyp2.middle_hand.append(dummy.draw(1))
        while len(dummyp2.bottom_hand)<5:
            dummyp2.bottom_hand.append(dummy.draw(1))
                   
        s = dummyp1.score(dummyp2)
        score += s
        
    #average scores and ranks
    av_score = score/n
    
        
    return av_score

                
def hands_to_board(hand1,hand2):
    
    full_deck = []

    for suit, val in Card.CHAR_SUIT_TO_INT_SUIT.items():
        for rank in Card.STR_RANKS:
                    full_deck.append(Card.new(rank + suit))
    
    board = np.zeros(52)
    
    for card in hand1.top_hand:
        board[full_deck.index(card)] = 1
        
    for card in hand1.middle_hand:
        board[full_deck.index(card)] = 2
        
    for card in hand1.bottom_hand:
        board[full_deck.index(card)] = 3

    for card in hand1.discards:
        board[full_deck.index(card)] = 4
        
    for card in hand1.dealt_cards:
        board[full_deck.index(card)] = 5
    
    for card in hand2.top_hand:
        board[full_deck.index(card)] = -1
        
    for card in hand2.middle_hand:
        board[full_deck.index(card)] = -2
        
    for card in hand2.bottom_hand:
        board[full_deck.index(card)] = -3    

    return np.array(board)



def board_to_hands(board,hand1,hand2):
    hand1.reset()
    hand2.reset()
    #board = np.array(board)
    #board = list(board)
    unseen = []
    full_deck = []

    for suit, val in Card.CHAR_SUIT_TO_INT_SUIT.items():
        for rank in Card.STR_RANKS:
                    full_deck.append(Card.new(rank + suit))
    
    BOARD_TO_HAND = {0:unseen,
                     1:hand1.top_hand,
                     2:hand1.middle_hand,
                     3:hand1.bottom_hand,
                     4:hand1.discards,
                     5:hand1.dealt_cards,
                     -1:hand2.top_hand,
                     -2:hand2.middle_hand,
                     -3:hand2.bottom_hand,
                     -4:hand2.discards,
                     -5:hand2.dealt_cards}
    print(board)
    for i in range(52):
        BOARD_TO_HAND[board[i]].append(full_deck[i])
        
    board = np.array(board)
    board = board[np.newaxis,:]

