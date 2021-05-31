import sys
sys.path.append("..") # Adds higher directory to python modules path.

from deck import *
from limit_holdem import *
from enum import Enum

class Test(Enum):
    FAIL = 0
    PASS = 1

def get_hand_rank_UT():

    UT = Test.PASS

    holdem = Limit_Holdem(2)
    
    straight_flush_list = sort_cards([Card(0,3), Card(0,4), Card(0,5), Card(0,6), Card(0,7), Card(2,12), Card(0,3)])
    four_of_a_kind_list = sort_cards([Card(0,3), Card(1,3), Card(2,3), Card(2,12), Card(3,7), Card(2,12), Card(0,3)])
    full_house_list = sort_cards([Card(0,0), Card(1,0), Card(2,0), Card(2,12), Card(3,7), Card(2,12), Card(0,3)])

    flush_hand_list = sort_cards([Card(0,2), Card(3,0)])
    flush_public_list = sort_cards([Card(2,0), Card(0,4), Card(0,3),  Card(0,2), Card(0,1)])
    
    straight_list = sort_cards([Card(0,0), Card(1,0), Card(2,4), Card(2,3), Card(3,2), Card(2,2), Card(0,1)])
    three_of_a_kind_list = sort_cards([Card(0,3), Card(1,0), Card(2,2), Card(2,3), Card(3,7), Card(2,6), Card(1,3)])
    two_pair_list = sort_cards([Card(0,0), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,7), Card(0,3)])
    one_pair_list = sort_cards([Card(0,0), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,6), Card(0,3)])
    high_card_list = sort_cards([Card(0,0), Card(1,2), Card(2,4), Card(3,6), Card(3,8), Card(2,10), Card(1,12)])

    hand_rank, high_card = holdem.get_hand_rank(straight_flush_list, [])
    if(hand_rank != 8 and high_card != 7):
        print("get_hand_rank_UT fail: straight_flush: " + str(hand_rank) + ", " + str(high_card))
        UT = Test.FAIL

    hand_rank, high_card = holdem.get_hand_rank(four_of_a_kind_list, [])
    if(hand_rank != 7 and high_card != 3):
        print("get_hand_rank_UT fail: four_of_a_kind: " + str(hand_rank) + ", " + str(high_card))
        UT = Test.FAIL

    hand_rank, high_card = holdem.get_hand_rank(full_house_list, [])
    if(hand_rank != 6 and high_card != 0):
        print("get_hand_rank_UT fail: full_house: " + str(hand_rank) + ", " + str(high_card))
        UT = Test.FAIL

    hand_rank, high_card = holdem.get_hand_rank(flush_hand_list, flush_public_list)
    if(hand_rank != 5 and high_card != 0):
        print("get_hand_rank_UT fail: flush: " + str(hand_rank) + ", " + str(high_card))
        UT = Test.FAIL

    hand_rank, high_card = holdem.get_hand_rank(straight_list, [])
    if(hand_rank != 4 and high_card != 4):
        print("get_hand_rank_UT fail: straight: " + str(hand_rank) + ", " + str(high_card))
        UT = Test.FAIL

    hand_rank, high_card = holdem.get_hand_rank(three_of_a_kind_list, [])
    if(hand_rank != 3 and high_card != 3):
        print("get_hand_rank_UT fail: three_of_a_kind: " + str(hand_rank) + ", " + str(high_card))
        UT = Test.FAIL

    hand_rank, high_card = holdem.get_hand_rank(two_pair_list, [])
    if(hand_rank != 2 and high_card != 0):
        print("get_hand_rank_UT fail: two_pair: " + str(hand_rank) + ", " + str(high_card))
        UT = Test.FAIL

    hand_rank, high_card = holdem.get_hand_rank(one_pair_list, [])
    if(hand_rank != 1 and high_card != 0):
        print("get_hand_rank_UT fail: one_pair: " + str(hand_rank) + ", " + str(high_card))
        UT = Test.FAIL

    
    hand_rank, high_card = holdem.get_hand_rank(high_card_list, [])
    if(hand_rank != 0 and high_card != 0):
        print("get_hand_rank_UT fail: high_card: " + str(hand_rank) + ", " + str(high_card))
        UT = Test.FAIL

    if(UT == Test.PASS):
        print("get_hand_rank_UT PASS")
    else:
        print("get_hand_rank_UT FAIL")    
    
def is_straight_flush_UT():

    UT = Test.PASS

    holdem = Limit_Holdem(2)
    
    # positive cases
    hand = [Card(0,3), Card(0,4)]
    public = [Card(0,5), Card(0,6), Card(0,7), Card(2,12), Card(0,3)]
    straight_flush, high_card = holdem.is_straight_flush(hand, public) # sraight flush
    if(straight_flush != True or high_card != 7):
        UT = Test.FAIL
        print("is_straight_flush_UT #1 FAILURE " + str(straight_flush) + ", " + str(high_card))

    hand = [Card(2,3), Card(2,4)]
    public = [Card(2,5), Card(2,6), Card(2,7), Card(2,8), Card(2,9)]
    straight_flush, high_card = holdem.is_straight_flush(hand, public)  # all cards make straight flush
    if(straight_flush != True or high_card != 9):
        UT = Test.FAIL
        print("is_straight_flush_UT #2 FAILURE " + str(straight_flush) + ", " + str(high_card))
        
    hand = [Card(2,0), Card(2,1)]
    public = [Card(2,2), Card(2,3), Card(2,4), Card(1,8), Card(0,12)]
    straight_flush, high_card = holdem.is_straight_flush(hand, public)  # ace low
    if(straight_flush != True or high_card != 4):
        UT = Test.FAIL
        print("is_straight_flush_UT #3 FAILURE " + str(straight_flush) + ", " + str(high_card))

    hand = [Card(2,0), Card(2,13)]
    public = [Card(2,12), Card(2,11), Card(2,10), Card(1,8), Card(0,12)]
    straight_flush, high_card = holdem.is_straight_flush(hand, public)  # ace high
    if(straight_flush != True or high_card != 0):
        UT = Test.FAIL
        print("is_straight_flush_UT #4 FAILURE " + str(straight_flush) + ", " + str(high_card))
        
    # negative cases
    hand = [Card(0,4), Card(1,5)]
    public = [Card(2,6), Card(2,7), Card(3,8), Card(2,6), Card(0,3)]
    straight_flush, high_card = holdem.is_straight_flush(hand, public) # straight, no flush
    if(straight_flush != False or high_card != None):
        UT = Test.FAIL
        print("is_straight_flush_UT #5 FAILURE " + str(straight_flush) + ", " + str(high_card))

    hand = [Card(3,0), Card(3,0)]
    public = [Card(3,2), Card(3,11), Card(3,7), Card(2,7), Card(0,3)]
    straight_flush, high_card = holdem.is_straight_flush(hand, public) # flush, no straight
    if(straight_flush != False or high_card != None):
        UT = Test.FAIL
        print("is_straight_flush_UT #6 FAILURE " + str(straight_flush) + ", " + str(high_card))

    hand = [Card(0,3), Card(0,2)]
    public = [Card(1,2), Card(1,11), Card(2,7), Card(2,7), Card(3,3)]
    straight_flush, high_card = holdem.is_straight_flush(hand, public) # no flush or straight
    if(straight_flush != False or high_card != None):
        UT = Test.FAIL
        print("is_straight_flush_UT #7 FAILURE " + str(straight_flush) + ", " + str(high_card))
    
    if(UT == Test.PASS):
        print("is_straight_flush_UT PASS")
    else:
        print("is_straight_flush_UT FAIL")    

def is_four_of_a_kind_UT():
    UT = Test.PASS

    holdem = Limit_Holdem(2)
    
    # positive cases
    four_of_a_kind, high_card = holdem.is_four_of_a_kind(sort_cards([Card(0,3), Card(1,3), Card(2,3), Card(2,12), Card(3,7), Card(2,12), Card(0,3)]))  # four of a kind
    if(four_of_a_kind != True or high_card != 3):
        UT = Test.FAIL
        print("is_four_of_a_kind_UT #1 FAILURE " + str(four_of_a_kind) + ", " + str(high_card))
    four_of_a_kind, high_card = holdem.is_four_of_a_kind(sort_cards([Card(0,0), Card(1,0), Card(2,0), Card(2,0), Card(3,12), Card(2,12), Card(0,12)])) # 4 of a kind and 3 of a kind
    if(four_of_a_kind != True or high_card != 0):
        UT = Test.FAIL
        print("is_four_of_a_kind_UT #2 FAILURE " + str(four_of_a_kind) + ", " + str(high_card))

    # negative cases
    four_of_a_kind, high_card = holdem.is_four_of_a_kind(sort_cards([Card(0,4), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,6), Card(0,3)])) # no matching ranks
    if(four_of_a_kind != False or high_card != None):
        UT = Test.FAIL
        print("is_four_of_a_kind_UT #3 FAILURE " + str(four_of_a_kind) + ", " + str(high_card))
    four_of_a_kind, high_card = holdem.is_four_of_a_kind(sort_cards([Card(0,0), Card(1,0), Card(2,2), Card(2,0), Card(3,7), Card(2,7), Card(0,3)])) # 3 of a kind
    if(four_of_a_kind != False or high_card != None):
        UT = Test.FAIL
        print("is_four_of_a_kind_UT #4 FAILURE " + str(four_of_a_kind) + ", " + str(high_card))
        
    if(UT == Test.PASS):
        print("is_four_of_a_kind_UT PASS")
    else:
        print("is_four_of_a_kind_UT FAIL")    

def is_full_house_UT():
    UT = Test.PASS

    holdem = Limit_Holdem(2)
    
    # positive cases
    full_house, high_card = holdem.is_full_house(sort_cards([Card(0,0), Card(1,0), Card(2,0), Card(2,12), Card(3,7), Card(2,12), Card(0,3)]))  # full house, ace high
    if(full_house != True or high_card != 0):
        UT = Test.FAIL
        print("is_full_house_UT #1 FAILURE " + str(full_house) + ", " + str(high_card))
    full_house, high_card = holdem.is_full_house(sort_cards([Card(0,0), Card(1,0), Card(2,0), Card(2,0), Card(3,12), Card(2,12), Card(0,12)])) # 4 of a kind and 3 of a kind, ace high
    if(full_house != True or high_card != 0):
        UT = Test.FAIL
        print("is_full_house_UT #2 FAILURE " + str(full_house) + ", " + str(high_card))

    # negative cases
    full_house, high_card = holdem.is_full_house(sort_cards([Card(0,4), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,6), Card(0,3)])) # no full house
    if(full_house != False or high_card != None):
        UT = Test.FAIL
        print("is_full_house_UT #3 FAILURE " + str(full_house) + ", " + str(high_card))
    full_house, high_card = holdem.is_full_house(sort_cards([Card(0,0), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,7), Card(0,3)])) # two pair
    if(full_house != False or high_card != None):
        UT = Test.FAIL
        print("is_full_house_UT #4 FAILURE " + str(full_house) + ", " + str(high_card))
    
    if(UT== Test.PASS):
        print("is_full_house_UT PASS")
    else:
        print("is_full_house_UT FAIL")    

def is_three_of_a_kind_UT():
    UT = Test.PASS

    holdem = Limit_Holdem(2)
    
    # positive cases
    three_of_a_kind, high_card = holdem.is_three_of_a_kind(sort_cards([Card(0,3), Card(1,0), Card(2,2), Card(2,3), Card(3,7), Card(2,6), Card(0,3)])) # three of a kind
    if(three_of_a_kind != True or high_card != 3):
        UT = Test.FAIL
        print("is_three_of_a_kind_UT #1 FAILURE " + str(three_of_a_kind) + ", " + str(high_card))
    three_of_a_kind, high_card = holdem.is_three_of_a_kind(sort_cards([Card(1,3), Card(1,2), Card(1,0), Card(2,3), Card(3,0), Card(2,0), Card(0,3)])) # two three of a kinds, high ace
    if(three_of_a_kind != True or high_card != 0):
        UT = Test.FAIL
        print("is_three_of_a_kind_UT #2 FAILURE " + str(three_of_a_kind) + ", " + str(high_card))
        
    # negative cases
    three_of_a_kind, high_card = holdem.is_three_of_a_kind(sort_cards([Card(0,4), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,6), Card(0,3)])) # no three of a kind
    if(three_of_a_kind != False or high_card != None):
        UT = Test.FAIL
        print("is_three_of_a_kind_UT #3 FAILURE " + str(three_of_a_kind) + ", " + str(high_card))

    
    if(UT == Test.PASS):
        print("is_three_of_a_kind_UT PASS")
    else:
        print("is_three_of_a_kind_UT FAIL")    

def is_pair_UT():
    UT = Test.PASS

    holdem = Limit_Holdem(2)
    
    # positive cases
    pair, high_card = holdem.is_pair(sort_cards([Card(0,0), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,6), Card(0,3)])) # one pair
    if(pair != True or high_card != 0):
        UT = Test.FAIL
        print("is_pair_UT #1 FAILURE " + str(pair) + ", " + str(high_card))

    # negative cases
    pair, high_card = holdem.is_pair(sort_cards([Card(0,4), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,6), Card(0,3)])) # no pair
    if(pair != False or high_card != None):
        UT = Test.FAIL
        print("is_pair_UT #2 FAILURE " + str(pair) + ", " + str(high_card))
        
    if(UT == Test.PASS):
        print("is_pair_UT PASS")
    else:
        print("is_pair_UT FAIL")            
        
def is_two_pair_UT():
    UT = Test.PASS

    holdem = Limit_Holdem(2)
    
    # positive cases
    two_pair, high_card = holdem.is_two_pair(sort_cards([Card(0,0), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,7), Card(0,3)]))  # two pair, high ace
    if(two_pair != True or high_card != 0):
        UT = Test.FAIL
        print("is_two_pair_UT #1 FAILURE " + str(two_pair) + ", " + str(high_card))
    two_pair, high_card = holdem.is_two_pair(sort_cards([Card(0,0), Card(1,0), Card(2,12), Card(2,12), Card(3,7), Card(2,6), Card(0,6)])) # three pair
    if(two_pair != True or high_card != 0):
        UT = Test.FAIL
        print("is_two_pair_UT #2 FAILURE " + str(two_pair) + ", " + str(high_card))
        
    # negative cases
    two_pair, high_card = holdem.is_two_pair(sort_cards([Card(0,4), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,6), Card(0,3)])) # no pair
    if(two_pair != False or high_card != None):
        UT = Test.FAIL
        print("is_two_pair_UT #3 FAILURE " + str(two_pair) + ", " + str(high_card))
    two_pair, high_card = holdem.is_two_pair(sort_cards([Card(0,0), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,6), Card(0,3)])) # one pair
    if(two_pair != False or high_card != None):
        UT = Test.FAIL
        print("is_two_pair_UT #4 FAILURE " + str(two_pair) + ", " + str(high_card))
    
    if(UT == Test.PASS):
        print("is_two_pair_UT PASS")
    else:
        print("is_two_pair_UT FAIL")                

def is_flush_UT():
    UT = Test.PASS

    holdem = Limit_Holdem(2)
    
    # positive cases

    # high card ace in hand
    hand = [Card(0,0), Card(0,2)]
    public = [Card(0,4), Card(0,3), Card(0,2), Card(0,2), Card(0,1)]
    
    flush, high_card = holdem.is_flush(hand, public) # 7 cards of same suit
    if(flush != True or high_card != 0):
        UT = Test.FAIL
        print("is_flush_UT #1 FAILURE " + str(flush) + ", " + str(high_card))

    # high card not in hand, but should return a high card of 3 as that's the highest in hand
    hand = [Card(0,3), Card(0,2)]
    public = [Card(3,0), Card(2,0), Card(0,4), Card(0,2), Card(0,0)]
    flush, high_card = holdem.is_flush(hand, public)  # 5 cards of same suit
    if(flush != True or high_card != 3):
        UT = Test.FAIL
        print("is_flush_UT #2 FAILURE " + str(flush) + ", " + str(high_card))

    
    # negative cases
    hand = [Card(0,4), Card(1,0)]
    public = [Card(2,2), Card(0,12), Card(0,7), Card(2,6), Card(2,3)]    
    flush, high_card = holdem.is_flush(hand, public) # 3 cards of same suit
    if(flush != False or high_card != None):
        UT = Test.FAIL
        print("is_flush_UT #3 FAILURE " + str(flush) + ", " + str(high_card))
        
    hand = [Card(3,4), Card(3,0)]
    public = [Card(2,2), Card(1,12), Card(0,7)]
    flush, high_card = holdem.is_flush(hand, public) # 2 cards of same suit
    if(flush != False or high_card != None):
        UT = Test.FAIL
        print("is_flush_UT #4 FAILURE " + str(flush) + ", " + str(high_card))
        
    hand = [Card(0,4), Card(1,0)]
    public = [Card(2,2), Card(3,12)]    
    flush, high_card = holdem.is_flush(hand, public) # 0 cards of same suit
    if(flush != False or high_card != None):
        UT = Test.FAIL
        print("is_flush_UT #5 FAILURE " + str(flush) + ", " + str(high_card))
        
    hand = [Card(0,0), Card(1,0)]
    public = [Card(2,4), Card(0,3), Card(0,2), Card(2,2), Card(0,1)]
    flush, high_card = holdem.is_flush(hand, public)  # 4 cards of same suit
    if(flush != False or high_card != None):
        UT = Test.FAIL
        print("is_flush_UT #6 FAILURE " + str(flush) + ", " + str(high_card))

    if(UT == Test.PASS):
        print("is_flush_UT PASS")
    else:
        print("is_flush_UT FAIL")            

def is_straight_UT():
    UT = Test.PASS

    holdem = Limit_Holdem(2)
    
    # positive cases
    straight, high_card = holdem.is_straight(sort_cards([Card(0,0), Card(1,0), Card(2,4), Card(2,3), Card(3,2), Card(2,2), Card(0,1)]))   # straight with some duplicates, low card ace
    if(straight != True or high_card != 4):
        UT = Test.FAIL
        print("is_straight_UT #1 FAILURE: " + str(straight) + ", " + str(high_card))

    straight, high_card = holdem.is_straight(sort_cards([Card(0,12), Card(1,0), Card(2,4), Card(2,3), Card(3,11), Card(2,2), Card(0,1)])) # straight with no duplicates, low card ace
    if(straight != True or high_card != 4):
        UT = Test.FAIL
        print("is_straight_UT #2 FAILURE " + str(straight) + ", " + str(high_card))

    straight, high_card = holdem.is_straight(sort_cards([Card(0,0), Card(1,13), Card(2,12), Card(2,11), Card(3,10), Card(2,2), Card(0,1)])) # straight with high card ace
    if(straight != True or high_card != 0):
        UT = Test.FAIL
        print("is_straight_UT #3 FAILURE " + str(straight) + ", " + str(high_card))
        
    # negative cases
    straight, high_card = holdem.is_straight(sort_cards([Card(0,4), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,6), Card(0,3)])) # 3 cards to a straight
    if(straight != False or high_card != None):
        UT = Test.FAIL
        print("is_straight_UT #4 FAILURE " + str(straight) + ", " + str(high_card))

    straight, high_card = holdem.is_straight(sort_cards([Card(0,4), Card(1,1), Card(2,2), Card(2,12), Card(3,7), Card(2,6), Card(0,3)])) # 4 cards to a straight
    if(straight != False or high_card != None):
        UT = Test.FAIL
        print("is_straight_UT #5 FAILURE " + str(straight) + ", " + str(high_card))


    if(UT == Test.PASS):
        print("is_straight_UT PASS")
    else:
        print("is_straight_UT FAIL")            

def limit_holdem_UT():
    UT_func_list = [get_hand_rank_UT, is_straight_flush_UT, is_four_of_a_kind_UT, is_full_house_UT, is_three_of_a_kind_UT, is_pair_UT, is_two_pair_UT, is_flush_UT, is_straight_UT]

    for function in UT_func_list:
        function()
        


if(__name__ == "__main__"):
    limit_holdem_UT()
