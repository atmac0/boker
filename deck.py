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
                if(card_list[i].rank == card_list[i+1].rank):
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
def get_hand_rank(hand, public_cards):
    all_cards = hand + public_cards
    sorted_cards = sort_cards(all_cards)

    straight_flush, high_card_rank = is_straight_flush(hand, public_cards)
    
    if(straight_flush):
        return 8, high_card_rank

    four_of_a_kind, high_card_rank = is_four_of_a_kind(sorted_cards)
   
    if(four_of_a_kind):
        return 7, high_card_rank
    
    full_house, high_card_rank = is_full_house(sorted_cards)
   
    if(full_house):
        return 6, high_card_rank

    flush, high_card_rank = is_flush(hand, public_cards)
   
    if(flush):
        return 5, high_card_rank

    straight, high_card_rank = is_straight(sorted_cards)
   
    if(straight):
        return 4, high_card_rank

    three_of_a_kind, high_card_rank = is_three_of_a_kind(sorted_cards)
    if(three_of_a_kind):
        return 3, high_card_rank

    two_pair, high_card_rank = is_two_pair(sorted_cards)
    if(two_pair):
        return 2, high_card_rank

    pair, high_card_rank = is_pair(sorted_cards)
    if(pair):
        return 1, high_card_rank
    
    return 0, get_high_card(hand)


def get_high_card(cards):
    max_rank = cards[0].rank
    
    for card in cards:
        if(card.rank > max_rank):
            max_rank = card.rank

    return max_rank

def is_straight_flush(hand, public):

    all_cards = hand + public
    
    if(len(all_cards) < 5):
        return False, None

    suit_counter = [[] for i in range(0, NUM_SUITS)]
    flush_suit = None
    high_card_rank = None

    # first discover if a flush exists.
    for card in all_cards:
        suit_counter[card.suit].append(card)
        if(len(suit_counter[card.suit]) == 5):
            flush_suit = card.suit

    if(flush_suit == None):
        return False, None

    sorted_flush_cards = sort_cards(suit_counter[flush_suit])
            
    consecutive_counter = 1
    consecutive_cards = [sorted_flush_cards[0]]
    high_card_rank = None

    # then, discover if the flush is also a straight
    for i in range(1, len(sorted_flush_cards)):
        if(sorted_flush_cards[i].rank == sorted_flush_cards[i-1].rank + 1):
            consecutive_counter += 1
            consecutive_cards.append(sorted_flush_cards[i])
        elif(sorted_flush_cards[i].rank == sorted_flush_cards[i-1].rank):
            consecutive_cards.append(sorted_flush_cards[i])
        else:
            consecutive_counter = 1
            consecutive_cards = []

        if(consecutive_counter >= 5):
            high_card_rank = sorted_flush_cards[i].rank


    if(high_card_rank != None):
        return True, high_card_rank
    
    return False, None
    
# returns True if a four of a kind is present. False if not.
def is_four_of_a_kind(sorted_cards):
    if(len(sorted_cards) < 4):
       return False
    
    for i in range(0, len(sorted_cards) - 3):
        if(sorted_cards[i].rank == sorted_cards[i+1].rank == sorted_cards[i+2].rank == sorted_cards[i+3].rank):
            return True, sorted_cards[i].rank
                
    return False, None
    
# determine if a deck is a full house. First, determine if a 3 of a kinds is present. If it is, delete the cards from the list. Then determine if a pair exists.
def is_full_house(sorted_cards):
    if(len(sorted_cards) < 5):
        return False, None    
    
    three_of_a_kind = False
    three_of_a_kind_rank = None
    pair_rank = None
    
    for i in range(0, len(sorted_cards) - 2):
        if(sorted_cards[i].rank == sorted_cards[i+1].rank == sorted_cards[i+2].rank):
            three_of_a_kind = True
            three_of_a_kind_rank = sorted_cards[i].rank
            sorted_cards[i:i+2] = []
            break

    pair, pair_rank = is_pair(sorted_cards)

    if(three_of_a_kind and pair):
        if(three_of_a_kind_rank > pair_rank):
            return True, three_of_a_kind_rank
        else:
            return True, pair_rank

    return False, None


# returns True if a TOAK is present. False if not.
def is_three_of_a_kind(sorted_cards):
    if(len(sorted_cards) < 3):
        return False, None
    
    for i in range(0, len(sorted_cards) - 2):
        if(sorted_cards[i].rank == sorted_cards[i+1].rank == sorted_cards[i+2].rank):
            return True, sorted_cards[i].rank
                
    return False, None

# returns True if a pair is present, along with rank of card if a pair is present. False if not. 
def is_pair(sorted_cards):
    if(len(sorted_cards) < 2):
        return False, None

    pair_rank = None
    
    for i in range(0, len(sorted_cards) - 1):
        if(sorted_cards[i].rank == sorted_cards[i+1].rank):
            if(pair_rank == None):
                pair_rank = sorted_cards[i].rank
            elif(sorted_cards[i].rank > pair_rank):
                pair_rank = sorted_cards[i].rank

    if(pair_rank != None):
        return True, pair_rank
    else:
        return False, pair_rank

# returns True if a pair is present. False if not.
# determines the rank of the first pair. If a pair of a different rank exists, a two pair exists
# returns True if a pair is present. False if not.
def is_two_pair(sorted_cards):
    if(len(sorted_cards) < 4):
        return False, None
    
    pairs_found = 0

    rank_of_high_pair = None
    
    for i in range(0, len(sorted_cards) - 1):
        if(sorted_cards[i].rank == sorted_cards[i+1].rank):
            pairs_found += 1
            if(rank_of_high_pair == None):
                rank_of_high_pair = sorted_cards[i].rank
            elif(sorted_cards[i].rank > rank_of_high_pair):
                rank_of_high_pair = sorted_cards[i].rank


    if(pairs_found >= 2):
        return True, rank_of_high_pair
    else:
        return False, rank_of_high_pair


# detemine if a hand is a flush
# count all the cards of each suit. If one of the counts is 5 or above, the hand is a flush
# returns: None if no flush is present.
#          An integer corresponding to the suit of the flush if there is a flush
def is_flush(hand, public_cards):

    all_cards = hand + public_cards
    
    if(len(all_cards) < 5):
        return False, None
    
    suit_counter = [0 for i in range(0, NUM_SUITS)]
    flush_suit = None
    high_card_rank = None
    
    for card in all_cards:
        suit_counter[card.suit] += 1
        if(suit_counter[card.suit] == 5):
            flush_suit = card.suit

    # find the high card of flush in the players hand if a flush exists. This is the high card of the player in a tie scenario
    if(flush_suit != None):
        for card in hand:
            if(card.suit == flush_suit):
                if(high_card_rank == None):
                    high_card_rank = card.rank
                elif(card.rank > high_card_rank):
                    high_card_rank = card.rank

    if(flush_suit != None):
        return True, high_card_rank
    else:
        return False, high_card_rank

def is_straight(sorted_cards):
    if(len(sorted_cards) < 5):
        return False, None
    
    consecutive_counter = 1
    previous_val = sorted_cards[0].rank
    high_card_rank = None

    
    for card in sorted_cards[1:]:
        if(card.rank == previous_val + 1):
            consecutive_counter += 1
        elif(card.rank == previous_val):
            pass
        else:
            consecutive_counter = 1

        # since the card list is sorted, each subsequent card that continues the straight is gauranteed to be of a higher rank
        if(consecutive_counter >= 5):
            high_card_card_rank = card.rank

        previous_val = card.rank

    if(high_card_rank != None):
        return True, high_card_rank
    else:
        return False, high_card_rank

