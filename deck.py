import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

        #def suit(self):
        #return self.suit

        #def rank(self):
        #return self.rank

class Deck:

    def __init__(self):
        
        self.deck = []
        self.init_deck()
        self.shuffle()

        # current location in deck
        self.deck_counter = 0

        
    def init_deck(self):

        deck = []
        
        #ace is 0, king is 13. hand evaluater will handle ace being both high and low
        for rank in range(0, 13):
            #0: spade, 1: club, 2: diamons, 3: hearts
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
