from deck import *

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

    def __init__(self, num_players, buy_in, big_blind, little_blind):
        self.num_players     = num_players
        self.players         = [Player() for i in range(0, self.num_players)]
        
        self.big_blind       = big_blind
        self.little_blind    = little_blind
        self.blind_counter   = 0
        
        self.pot             = 0

        for player in self.players:
            player.cash_stack = buy_in

        self.deck            = Deck()
        self.community_cards = []        

    # deal the hands. make pertinant players 
    def deal_hands(self):
        for player_num in range(0, self.num_players):
            # each hand is a tuple of 2 cards
            self.players.hand = (self.deck.draw(), self.deck.draw())
        "TODO: place the blind bets if the players aren't losers"
        

    def deal_community(self):
        num_community = len(self.community_cards)

        # deal flop
        if(num_community == 0):
            self.community_cards.append(self.deck.draw())
            self.community_cards.append(self.deck.draw())
            self.community_cards.append(self.deck.draw())
        # deal turn or the river
        elif(num_community > 0 and num_community < 5):
            self.community_cards.append(self.deck.draw())
        else:
            print('Error in dealing community: {0} cards in community pool'.format(num_community))

        # reset the players bet for this round
        for player in self.players:
            player.current_bet = 0

    def view_community(self):
        return self.community_cards

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
        self.community_cards = []
        self.deck.shuffle()
        
        self.blind_counter   = self.blind_counter + 1
        # reset the blind counter back to the beginning
        if(self.blind_counter == self.num_players):
            self.blind_counter = 0

        for player in self.players:
            player.reset()
    
holdem = Holdem(5, 10000, 100, 50)
