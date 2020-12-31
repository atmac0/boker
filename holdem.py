from deck import *

NUM_CARDS_IN_FLOP

class Player:

    def __init__(self):
        self.hand        = None
        self.folded      = False
        self.loser       = False
        self.current_bet = 0
        self.cash_stack  = 0

    def reset(self):
        self.hand        = None
        self.folded      = False
        self.current_bet = 0
        
class Holdem:

    def __init__(self, num_players, big_blind, little_blind):
        self.num_players   = num_players
        self.players       = [Player() for i in range(0, self.num_players)]
        
        self.big_blind     = big_blind
        self.little_blind  = little_blind
        
        self.pot           = 0

        self.raise_amount  = 0

        self.deck            = Deck()
        self.flop            = None
        self.turn            = None
        self.river           = None      

    # deal the hands. Make players pay the blinds.
    def deal_hands(self):

        self.players[self.big_blind_player].cash_stack = self.players[self.big_blind_player].cash_stack - self.big_blind
        self.players[self.little_blind_player].cash_stack = self.players[self.little_blind_player].cash_stack - self.little_blind

        self.players[self.big_blind_player].current_bet = self.players[self.big_blind_player].current_bet + self.big_blind
        self.players[self.little_blind_player].current_bet = self.players[self.little_blind_player].current_bet + self.little_blind

        self.pot = self.big_blind + self.little_blind
        
        for player_num in range(0, self.num_players):
            # each hand is a tuple of 2 cards
            self.players.hand = (self.deck.draw(), self.deck.draw())
        

    def deal_community(self):
        # deal flop
        if(self.flop == None):
            self.flop = [self.deck.draw() for x in range(0,NUM_CARDS_IN_FLOP)]
        # deal turn or the river
        elif(self.turn == None):
            self.turn = [self.deck.draw()]
        elif(self.river == None):
            self.river = [self.deck.draw()]
        else:
            print('Error in dealing community: flop, turn, and river already dealt')

        # reset the players bet for this round
        for player in self.players:
            player.current_bet = 0

    def get_hand(self, player_num):
        return self.players[player_num].hand

    def get_cashstack(self, player_num):
        return self.players[player_num].cash_stack

    def bet(self, player_num, bet_size):
        if(self.players[player_num].cash_stack < bet_size):
            print('Player {0} attempted to bet {1}. Player has only {2} in cash stack.'.format(player_num, bet_size, self.cash_stacks[player_num]))
        elif(bet_size < self.big_blind):
            print('Player {0} attempted to bet {1}. Big blind is {2}.'.format(player_num, bet_size, self.big_blind))
        else:
            self.cash_stacks[player_num] = self.cash_stacks[player_num] - bet_size
            self.pot = self.pot + bet_size
            self.players[player_num].current_bet = self.players[player_num].current_bet + bet_size

                
    def reset_game(self):
        self.pot             = 0
        self.flop = None
        self.turn = None
        self.river = None
        self.deck.shuffle()
        self.assign_blinds()
        
        for player in self.players:
            player.reset()

    def assign_blinds(self):
        self.big_blind_player        = self.big_blind_player + 1
        
        # skip all losing players for big blind
        while(self.players[self.big_blind_player].loser == True):
            self.big_blind_player    = self.big_blind_player + 1

        # reset the blind player back to the beginning
        if(self.big_blind_player == self.num_players):
            self.big_blind_player    = 0

        self.little_blind_player     = self.big_blind_player - 1

        # skip all losers for little blind
        # the counter will go into negative indexing, that is OK, it will still
        # represent the correct player
        while(self.players[self.little_blind_player].loser == True):
            self.little_blind_player = self.little_blind_player - 1

        # restore little blind counter to a positive if a negative index was used
        if(self.little_blind_player < 0):
            self.little_blind_player = self.num_players - self.little_blind_player
            
holdem = Holdem(5, 10000, 100, 50)
