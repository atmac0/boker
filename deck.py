import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    # string will be a unique value formatted as four numbers, representing suit/rank. For example, a jack (10) of hearts (3) will be represented as 1003
    def to_string(self):
        
        if(self.suit < 10):
            suit_string = '0' + str(self.suit)
        else:
            suit_string = str(self.suit)

        card_string = suit_string + '0' + str(self.rank)

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
        card = self.deck[self.deck_counter]
        self.deck_counter = self.deck_counter + 1

        return card
