from deck import *

class Player:

    def __init__(self):
        self.hand        = None
        self.folded      = False
        self.loser       = False
        self.checked     = False
        self.bet         = 0
        self.better      = False
        
class Limit_Holdem:

    def __init__(self, num_players, big_blind, little_blind):
        self.num_players   = num_players
        self.players       = [Player() for i in range(0, self.num_players)]
        
        self.big_blind     = big_blind
        self.little_blind  = little_blind
        
        self.pot           = 0
        self.num_bets      = 0
        
        self.deck            = Deck()
        
        self.game_phase = 'initial'
        
        self.flop = []
        self.turn  = None
        self.river  = None

        self.bet_counter = 0

        self.game_complete = False
        
    # deal the hands. Make players pay the blinds.
    def deal_hands(self):        
        for player_num in range(0, self.num_players):
            # each hand is a tuple of 2 cards
            self.players.hand = (self.deck.draw(), self.deck.draw())
        

    def deal_community(self):
        num_community = len(self.community_cards)

        # deal flop
        if(self.game_phase = 'initial'):
            self.flop.append(self.deck.draw())
            self.flop.append(self.deck.draw())
            self.flop.append(self.deck.draw())

            self.sort_flop()

            self.game_phase = 'flop'
            
        # deal turn 
        elif(self.game_phase = 'turn'):
            self.turn = self.deck.draw()
            self.game_phase = 'turn'
            
        # deal river
        elif(self.game_phase = 'turn'):
            self.river = self.deck.draw()
            self.game_phase = 'river'
        else:
            print('Error dealing cards, unexpected game phase of: ' + self.game_phase)


    # sort the flop acending by suit, then rank. So ace of spades will be before 9 of hearts, and 10 of diamonds will be after jack of clubs
    # suit ordering goes: spade, club, diamond, heart
    # rank ordering goes: 2->ace
    # this function is basically bubble sort, but for a size of 3 there was no reason to implement it with a loop
    # this needs to be sorted so we don't 
    def sort_flop():
        if(compare_cards(self.flop[0], self.flop[1])):
            self.flop[0], self.flop[1] = self.flop[1], self.flop[0]

        if(compare_cards(self.flop[1], self.flop[2])):
            self.flop[1], self.flop[2] = self.flop[2], self.flop[1]

    # returns true if the first card is greater than the second card
    def compare_cards(card1, card2):
           if(card1.suit > card2.suit):
               return True
           if(card1.suit < card2.suit):
               return False

           if(card1.rank > card2.rank):
               return True
           if(card1.rank < card2.rank):
               return False

           print("Duplicate card dealt in deck, something went wrong!")
           exit(0)
           
    def get_river(self):
        return self.river

    def get_turn(self):
        return self.turn

    def get_flop(self):
        return self.flop
    
    def get_hand(self, player_num):
        return self.players[player_num].hand

    def get_bet_counter(self):
        return self.bet_counter
    
    def get_game_phase(self):
        return self.game_phase

    def check(self, player_num):
        self.players[player_num].checked = True


    def uncheck_all(self):
        for player in self.players:
            player.checked = False
        
    def bet(self, player_num, bet_size):
        if(self.bet_counter < 4):
            self.players[player_num].bet = self.players[player_num].bet + bet_size
            self.pot = self.pot + bet_size
            self.bet_counter = self.bet_counter + 1
            self.uncheck_all()
        else:
            print("AI tried to bet when it was illegal, something went wrong")
            exit(0)


    def game_complete():
        return self.game_complete
            
holdem = Holdem(5, 10000, 100, 50)
