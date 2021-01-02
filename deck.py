import random

NUM_SUITS = 4
NUM_RANKS = 14

SPADE    = 0
CLUB     = 1
DIAMONDS = 2
HEARTS   = 3

ACE_LOW  = 0
ONE      = 1
TWO      = 2
THREE    = 3
FOUR     = 4
FIVE     = 5
SIX      = 6
SEVEN    = 7
EIGHT    = 8
NINE     = 9
TEN      = 10
JACK     = 11
QUEEN    = 12
KIND     = 13
ACE_HIGH = 14


class Card:
    def __init__(self, suit, rank):
        #0: spade, 1: club, 2: diamonds, 3: hearts
        self.suit = suit
        #ace is 0, king is 13. Ace may also be 14 when being used as a high card
        self.rank = rank
        
    # string will be a unique value formatted as four numbers, representing suit/rank. For example, a jack (10) of hearts (3) will be represented as 1003
    def to_string(self):

        suit_char = self.suit_num_to_char(self.suit)
        
        card_string = str(suit_char) + str(self.rank).zfill(2)

        return card_string


    def suit_num_to_char(self, suit_num):
        if(suit_num == SPADE):
            return 'S'
        if(suit_num == CLUB):
            return 'C'
        if(suit_num == DIAMONDS):
            return 'D'
        if(suit_num == HEARTS):
            return 'H'
        
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

    def remaining_cards(self):
        return self.deck[self.deck_counter:]
    
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

def print_card_list(card_list):
    print("PRINTING CARD LIST")
    for card in card_list:
        print("SUIT: " + str(card.suit) + " , RANK: " + str(card.rank))

def card_list_to_string(card_list):
    card_list_string = ''
    for card in card_list:
        card_list_string += card.to_string()

    return card_list_string

def same_card(card1, card2):
    if(card1.rank == card2.rank):
        if(card1.suit == card2.suit):
            return True
    return False
