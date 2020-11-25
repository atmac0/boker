import random

NUM_SUITS = 4
NUM_RANKS = 14

class Card:
    def __init__(self, suit, rank):
        #0: spade, 1: club, 2: diamonds, 3: hearts
        self.suit = suit
        #ace is 0, king is 13
        self.rank = rank
        
    # string will be a unique value formatted as four numbers, representing suit/rank. For example, a jack (10) of hearts (3) will be represented as 1003
    def to_string(self):

        card_string = str(self.suit).zfill(2) + str(self.rank).zfill(2)

        return card_string
        
class Deck:

    def __init__(self, shuffle=True):
        
        self.deck = []
        self.init_deck()
        if(shuffle):
            self.shuffle()

        # current location in deck
        self.deck_counter = 0

        
    def init_deck(self):

        deck = []
        
        #ace is 0, king is 13. hand evaluater will handle ace being both high and low
        for rank in range(0, 13):
            #0: spade, 1: club, 2: diamonds, 3: hearts
            for suit in range(0,4):
                card = Card(suit, rank)
                deck.append(card)

        self.deck = deck
            

    def print_deck(self):
        for card in self.deck:
            print('SUIT: {0}, RANK {1}'.format(card.suit, card.rank))

    def shuffle(self):
        self.deck_counter = 0
        random.shuffle(self.deck)
        
 
    def draw(self):
        if(self.deck_counter < 52):
            card = self.deck[self.deck_counter]
            self.deck_counter = self.deck_counter + 1
            return card
        else:
            print("Attempting to draw: no cards left in the deck")
            return None
        
    
# args: card_list - unsorted array of cards
# summary:
# sort cards high to low. This list will be a maximum size of 7
# cards will be sorted by rank first, then suit; e.g. 2 of hearts is greater than
# 6 of clubs. However 7 of diamonds is greater than 7 of spades
# this uses bubble sort. This could definitely be improved
def sort_cards(card_list):
    rank_sorted = False
    suit_sorted = False
    
    while(rank_sorted == False):
        swap_made = False
        for i in range(0, len(card_list)-1):
            if(card_list[i].rank > card_list[i+1].rank):
                temp_card = card_list[i]
                card_list[i] = card_list[i+1]
                card_list[i+1] = temp_card
                swap_made = True

        if(swap_made == False):
            rank_sorted = True


    while(suit_sorted == False):
        swap_made = False
        for i in range(0, len(card_list)-1):
            if(card_list[i].suit > card_list[i+1].suit):
                temp_card = card_list[i]
                card_list[i] = card_list[i+1]
                card_list[i+1] = temp_card
                swap_made = True

        if(swap_made == False):
            suit_sorted = True         

    return card_list

# hand ranks listed 0-8:
# 0: high card
# 1: one pair
# 2: two pair
# 3: three of a kind
# 4: straight
# 5: flush
# 6: full house
# 7: four of a kind
# 8: straight flush
def get_hand_rank(self, hand, public_cards):
    all_cards = hand + public_cards
    sorted_cards = sort_cards(all_cards)
    
    if(is_straight_flush(sorted_cards)):
       return 8
    if(is_four_of_a_kind(sorted_cards)):
       return 7
    if(is_full_house(sorted_cards)):
       return 6
    if(is_flsuh(sorted_cards)):
       return 5
    if(is_straight(sorted_cards)):
       return 4
    if(is_three_of_a_kind(sorted_cards)):
       return 3
    if(is_two_pair(sorted_cards)):
       return 2
    if(is_pair(sorted_cards)):
       return 1
    
    return 0




def is_straight_flush(sorted_cards):
    consecutive_counter = 1
    
    for i in range(1, len(sorted_cards)):
        if(sorted_cards[i].rank == sorted_cards[i-1] + 1):
            consecutive_counter += 1
        else:
            consecutive_counter = 1

        if(consecutive_counter == 5):
            if(is_flush(sorted_cards[i-5:i])):
                return True

    return False
    
# returns True if a four of a kind is present. False if not.
def is_four_of_a_kind(sorted_cards):
    for i in range(0, len(cards) - 3):
        if(sorted_cards[i] == sorted_cards[i+1] == sorted_cards[i+2] == sorted_cards[i+3]):
            return True
                
    return False
    
# determine if a deck is a full house. First, determine if a 3 of a kinds is present. If it is, delete the cards from the list. Then determine if a pair exists.
def is_full_house(sorted_cards):
    three_of_a_kind = False
    
    for i in range(0, len(cards) - 2):
        if(sorted_cards[i] == sorted_cards[i+1] == sorted_cards[i+2]):
            three_of_a_kind = True
            sorted_cards[i:i+2] = []

    pair = is_pair(sorted_cards)

    if(three_of_a_kind and pair):
        return True

    return False


# returns True if a TOAK is present. False if not.
def is_three_of_a_kind(sorted_cards):
    for i in range(0, len(cards) - 2):
        if(sorted_cards[i] == sorted_cards[i+1] == sorted_cards[i+2]):
            return True
                
    return False

# returns True if a pair is present. False if not.
def is_pair(sorted_cards):
    for i in range(0, len(sorted_cards) - 1):
        if(sorted_cards[i] == sorted_cards[i+1]):
            return True
                
    return False

# returns True if a pair is present. False if not.
# determines the rank of the first pair. If a pair of a different rank exists, a two pair exists
# returns True if a pair is present. False if not.
def is_two_pair(sorted_cards):
    rank_of_first_pair = None
    
    for i in range(0, len(cards) - 1):
        if(sorted_cards[i] == sorted_cards[i+1]):
            if(rank_of_first_pair == None):
                rank_of_first_pair = sorted_cards[i].rank
            elif(rank_of_first_pair != sorted_cards[i].rank):
                return True
                
    return False


# detemine if a hand is a flush
# count all the cards of each suit. If one of the counts is 5 or above, the hand is a flush
# returns: None if no flush is present.
#          An integer corresponding to the suit of the flush if there is a flush
def is_flush(cards):
    suit_counter = [0 for i in range(0, NUM_SUITS)]

    for card in cards:
        suit_counter[card.suit] += 1
        if(suit_counter[card.suit] == 5):
            return True
        
    return False

def is_straight(sorted_cards):
    consecutive_counter = 1
    previous_val = sorted_cards[0].rank
    
    for card in sorted_cards[1:]:
        if(card.rank == previous_val + 1):
            consecutive_counter += 1
        else:
            consecutive_counter = 1

        if(consecutive_counter == 5):
            return True

        previous_val = card.rank

    return False

