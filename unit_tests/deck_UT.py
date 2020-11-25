import sys
sys.path.append("..") # Adds higher directory to python modules path.

from deck import *
from enum import Enum

class Test(Enum):
    FAIL = 0
    PASS = 1

def card_class_UT():
    UT = Test.PASS
    
    for rank in range(0, NUM_RANKS):
        for suit in range(0, NUM_SUITS):
            test_card = Card(suit, rank)
            
            test_card_string = test_card.to_string()
            expected_string = str(suit).zfill(2) + str(rank).zfill(2)
            
            if(test_card_string != expected_string):
                print("card_class_UT failure: expected " + expected_string + ", " + test_card_string + " observed")
                UT = Test.FAIL

    if(UT == Test.PASS):
        print("card_class_UT PASS")
    else:
        print("card_class_UT FAIL")        

def deck_class_UT():
    pass

def sort_cards_UT():

    UT = Test.PASS
    
    card_list = [Card(3,5), Card(2,5), Card(1,13), Card(3,4), Card(2,12), Card(3,0), Card(2,0), Card(1,0), Card(0,0)]

    sorted_card_list = sort_cards(card_list)

    for i in range(0, len(sorted_card_list) - 1):
        current_card = sorted_card_list[i]
        next_card    = sorted_card_list[i+1]

        if(current_card.rank > next_card.rank):
            print("Failure in sort_cards_UT: current card rank: " + str(current_card.rank) + ", next card rank: " + str(next_card.rank))
            UT = Test.FAIL

        if(current_card.rank == next_card.rank):
            if(current_card.suit > next_card.suit):
                print("Failure in sort_cards_UT: rank of both: " + str(current_card.rank) + ", current card suit: " + str(current_card.suit) + ", next card suit: " + str(next_card.suit))
                UT = Test.FAIL

    if(UT == Test.PASS):
        print("sort_cards_UT PASS")
    else:
        print("sort_cards_UT FAIL")            
    

def get_hand_rank_UT():
    pass

def is_straight_flush_UT():
    pass

def is_four_of_a_kind_UT():
    pass

def is_full_house_UT():
    pass

def is_three_of_a_kind_UT():
    pass

def is_pair_UT():

    UT = Test.PASS
    
    pair_cards = [Card(0,0), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,6), Card(0,3)]
    no_pair_cards = [Card(0,4), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,6), Card(0,3)]

    sorted_pair_cards = sort_cards(pair_cards)
    sorted_no_pair_cards = sort_cards(no_pair_cards)

    if(is_pair(sorted_pair_cards) == False):
        UT = Test.FAIL
    if(is_pair(sorted_no_pair_cards) == True):
        UT = Test.FAIL

    if(UT == Test.PASS):
        print("is_pair_UT PASS")
    else:
        print("is_pair_UT FAIL")            
        
def is_two_pair_UT():
    pass

def is_flush_UT():
    pass

def is_straight_UT():
    pass


def deck_UT():
    UT_func_list = [card_class_UT, deck_class_UT, sort_cards_UT, get_hand_rank_UT, is_straight_flush_UT, is_four_of_a_kind_UT, is_full_house_UT, is_three_of_a_kind_UT, is_pair_UT, is_two_pair_UT, is_flush_UT, is_straight_UT]

    for function in UT_func_list:
        function()

if(__name__ == "__main__"):
    deck_UT()
