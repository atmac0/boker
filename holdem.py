from deck import *

class Holdem:

    def __init__(self, num_players, buy_in, big_blind, little_blind):
        self.num_players     = num_players

        self.big_blind       = big_blind
        self.little_blind    = little_blind

        self.pot             = 0
        self.cash_stacks     = []
        self.init_cash_stacks(buy_in)
        
        self.deck            = Deck()

        self.hands           = []
        self.community_cards = []
    
    def init_cash_stacks(self, buy_in):
        for player_num in range(0, self.num_players):
            self.cash_stacks.append(buy_in)

    def deal_hands(self):
        for player_num in range(0, self.num_players):
            # each hand is a tuple of 2 cards
            self.hand.append( (self.deck.draw(), self.deck.draw()) )

    def deal_community(self):
        num_community = len(self.community_cards)

        if(num_community == 0):
            self.community_cards
