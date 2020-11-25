from math import *
from itertools import *
import operator

import random

BIG_BLIND = 2
LITTLE_BLIND = 1
NUM_CARDS_IN_DECK = 52

class Node:
    # args: history            - array of all nodes to get to this node
    #       exploration_weight - integer marking the exploratin weight
    #       players_in_game    - list of booleans marking all players left in the game. Each index corresponds to a player, each boolean marks if they are still in the game
    #       acting_player      - integer marking the current acting player, used to index players_in_game. If acting player is -1, then the player is the dealer
    #       betting_round      - boolean describing if it is a betting round or not (betting round player chooses, non betting round dealer deals)
    #       flop, turn, river  - boolean values describing if the game has made it past the flop, the turn, or the river.
    #       bet_made           - integer value representing bet made by acting player
    #       card_drawn         - card object representing card drawn
    def __init__(self, history, exploration_weight, players_in_game, bet_made=None, card_drawn=None):
        self.history               = history
        self.exploration_weight    = exploration_weight
        self.players_in_game       = players_in_game
        self.acting_player         = self.find_acting_player()
        
        if(bet_made != None):
            self.bet_made          = bet_made
        else:
            assert card_drawn is not None
            self.card_drawn    = card_drawn

        self.num_players_in_game = get_num_players_in_game()
        
        # positive CRF is a good decision. negative CFR is a bad decision
        self.avg_CFR = 0
        self.visits = 0

        self.children = None

        self.current_round_string = self.get_current_round_string()


    # find current acting player by counting up from the previous acting player until you hit the next player still in the game
    def find_acting_player(self):
        player_counter = self.get_parent().acting_player

        num_total_players = len(self.players_in_game)
        
        while(player_counter < (num_total_players * 3)):
            player_counter += 1
            if(self.players_in_game[player_counter % num_total_players] == True):
                return player_counter

        raise Exception("COULD NOT FIND ACTING PLAYER, SOMETHING WENT WRONG!")
        
    def backprop_CFR(self):
        pass

    def make_children(self):
        
        if('betting' in self.current_round_string):
            self.make_children_betting()
        elif('draw' in self.current_round_string):
            self.make_children_drawing()
        else:
            raise Exception('ERROR IN MAKING CHILDREN. ILLEGAL CHILD: ' + next_round_string)

    def get_children(self):
        if(self.children is None):
            self.make_children()

        return self.children
    
    def make_children_betting(self):
        self.children = dict()
        valid_bets = self.calculate_valid_bets()

        for(bet in valid_bets):
            next_history = self.history.append(self)

            if(bet == -1):
                next_players_in_game = self.players_in_game.copy()
                next_players_in_game[self.acting_player] = False
                self.children[str(bet)] = Node(next_history, self.exploration_weight, next_players_in_game, bet_made=bet)
            else:
                self.children[str(bet)] = Node(next_history, self.exploration_weight, self.players_in_game, bet_made=bet)
        

        
    def make_children_drawing(self):
        self.children = dict()
        remaining_deck = self.calculate_valid_draws()

        for card in remaining_deck:
            card_string = card.to_string()

            next_history = self.history.append(self)
            self.children[card_string] = Node(next_history, self.exploration_weight, self.players_in_game, card_drawn=card)
        
    def next_acting_player(self):
        player_counter = self.acting_player

        num_total_players = len(self.players_in_game)

        # exit condition should only be satisfied in the case of an error
        while(player_counter < (num_total_players * 3) ):
            player_counter += 1
            if(self.players_in_game[player_counter % num_total_players] == True):
                return player_counter


        raise Exception("COULD NOT FIND NEXT ACTING PLAYER, SOMETHING WENT WRONG!")

                
    def bet_nodes_since_draw(self):
        nodes_in_round = []
                
        for node in reversed(self.history):
            if(node.betting_round = False):
                break
            nodes_in_round.append(node)

        if(nodes_in_round > 4):
            raise Exception('ERROR: NUMBER OF BETS SINCE DRAW EXCEEDED EXPECTED NUMBER OF 4')
            
        return nodes_in_round

    def num_bets_since_draw(self):
        return len(self.bet_notes_since_draw())
    
    def get_num_players_in_game(self):
        num_players_in_game = 0
        
        for player in self.num_players_in_game:
            if(player):
                num_players_in_game += 1

        return num_players_in_game


    # returns the number of cards drawn
    def num_cards_drawn(self):
        return len(self.cards_drawn())

    # returns a list of the cards drawn
    def cards_drawn(self):
        cards_drawn = []
        for node in self.history:
            if(node.betting_node == False):
                cards_drawn.append(node.card_drawn)

        return cards_drawn

    def is_node_terminal(self):
        # if all players but 1 have folded, the game has ended
        if(self.num_players_in_game == 1):
            return True

        # if all players have checked/bet in the river betting round, the game is over
        if((self.current_round_string == 'river_betting') and self.did_all_players_match_bet()):
            return True

        return False
        
    # determine the current round
    # returns: "pre_flop_betting"
    #          "flop_draw"
    #          "flop_betting"
    #          "turn_draw"
    #          "turn_betting"
    #          "river_draw"
    #          "river_betting"
    #          "terminal"
    def get_current_round_string(self):

        if(self.is_node_terminal()):
            return 'terminal'
        
        num_cards_drawn = self.num_cards_drawn()

        if(self.betting_round == True):
            elif(num_cards_drawn == 0):
                return 'pre_flop_betting'
            elif(num_cards_drawn == 3):
                return 'flop_betting'
            elif(num_cards_drawn == 4):
                return 'turn_betting'
            elif(num_cards_drawn == 5):
                return 'river_betting'
            else:
                raise Exception("ERROR IN CALCULATING CURRENT ROUND\nNUMBER OF CARDS DRAWN: " + str(num_cards_drawn) + "\nBETTING ROUND == " + str(self.betting_round))

        else:
            if(num_cards_drawn == 0):
                return 'flop_draw'
            elif(num_cards_drawn == 1):
                return 'flop_draw'
            elif(num_cards_drawn == 2):
                return 'flop_draw'
            elif(num_cards_drawn == 3):
                return 'turn_draw'
            elif(num_cards_drawn == 4):
                return 'river_draw'
            else:
                raise Exception("ERROR IN CALCULATING CURRENT ROUND\nNUMBER OF CARDS DRAWN: " + str(num_cards_drawn) + "\nBETTING ROUND == " + str(self.betting_round))
        
    
    # calculate all valid bets based on the history. This will be some multiple of the big blind. -1 is a fold
    def calculate_valid_bets(self):
        
        minimum_bet = self.minimum_bet()

        valid_bets = [-1, minimum_bet]
        
        if(self.num_bets_since_draw() < 4):
            can_raise = True
        else:
            can_raise = False

        if(can_raise == False):
            return valid_bets
            
        if(minimum_bet == LITTLE_BLIND):
            valid_bets.append(LITTLE_BLIND + BIG_BLIND)
        elif(minimum_bet == BIG_BLIND):
            valid_bets.append(BIG_BLIND * 2)
            
        return valid_bets
    

    def minimum_bet(self):
        bet_sums = self.sum_bets_in_round()
            
        maximum_bet_made = max(bet_sums.iteritem(), key=operator.itemgetter(1))[0]
        acting_player_bet = bet_sums[str(self.acting_player)]

        minimum_bet = maximum_bet_made - acting_player_bet

        assert minimum_bet >= 0
        
        return minimum_bet
    

    # returns a list, of which each element is a player number for each player still in the game
    def get_player_list(self):
        player_list = []
        for player_num in range(0, len(self.players_in_game)):
            if(self.players_in_game[player_num] == True):
                player_list.append(player_num)
        return player_list
                
    # calculate all cards that can be drawn based on the history
    # returns a list of all remaining cards
    def calculate_valid_draws(self):

        deck = Deck(shuffle=False)
        deck = deck.deck

        drawn_cards = 0
        
        for node in self.history:
            if(node.betting_node = False):
                drawn_cards += 1
                for card in deck:
                    if((node.card_drawn.suit == card.suit) and (node.card_drawn.rank == card.rank)):
                       deck.remove(card)
                       break

        assert len(deck) == (NUM_CARDS_IN_DECK - drawn_cards)

        return deck


    def get_num_players_remaining(self):
        num_players = 0
        for player in self.players_in_game:
            if(player):
                num_players += 1

        return num_players

    # see if all remaining players have matched the current bet
    def did_all_players_match_bet(self):

        if(self.betting_node == False):
            print("ATTEMPTED TO SEE IF ALL PLAYERS CHECKED DURING DRAWING ROUND")
            exit(0)

        # fist node represents first bet in round
        bet_nodes_in_round = self.bet_nodes_since_draw()

        # if all the players (counting from the start of the round) have yet to have an action, the round cannot be over
        if(len(bet_nodes_in_round) < bet_nodes_in_round[0].num_players_in_game):
            return False

        bet_sums = self.sum_bets_in_round()
        
        test_val = list(bet_sums.values())[0]
        
        for bet_sum in bet_sums:
            # in this case, each remaining player has not contributed equal amounts to the pot
            if(bet_sum != test_val):
                return False
        return True

    # return a dictionary of the sum of each players bets for the round
    def sum_bets_in_round():
        bet_nodes_in_round = self.bet_nodes_since_draw()
        bet_sums = dict()
        
        for betting_node in bet_nodes_in_round:
            if(betting_node.bet_made != -1):
                bet_sums[str(betting_node.acting_player)] += betting_node.bet_made

        return bet_sums

    
    # args: valid_bets - a list of integers of all valid bets
    def do_rollout(self):
        self.visits += 1

        if(self.is_betting_round()):
            choices = self.calculate_valid_bets()
            
        else: # dealer round
            choices = self.calculate_valid_draws()
        
        
        if(len(self.children) == 0):

            
            
            for bet in valid_bets:
                pass
                #self.children[str(bet)] = Node(self, self.exploration_weight, self.players_in_game, self.acting_player

    # selects a child node for a drawing round based on the least number of visits
    def select_child_draw(self):
        choice = self.children[0]

        for child in self.children:
            if(choice.visits < child.visits):
                choice = child

        return choice
                
    # selects a child node for a betting round based on the equation UCB1 = CFR/visits_of_child + exploration_weight*sqrt(ln(visits_of_parent)/visits_of_child)
    def select_child_betting(self):
        choice = None
        UCB1_of_choice = None

        # for all children, calculate the UCB1. Return the child with the largest UCB1
        for child in self.children:
            if(child.visits == 0):
                return child
            
            UCB1 = child.avg_CFR/child.visits + self.exploration_weight * sqrt( log(self.visits) / child.visits)

            if(choice == None):
                choice = child
                UCB1_of_choice = UCB1
            elif(UCB1 > UCB1_of_choice):
                choice = child
                UCB1_of_choice = UCB1

        return choice

    def get_random_child_key(self):
        if(self.children == None):
            self.make_children()

        return random.choice(self.children.keys())

    def get_child_node_from_key(self, key):
        if(self.children == None):
               print("CHILDREN NOT CREATED. CANNOT INDEX FOR KEY")
               exit(0)
        return self.children[key]

    def get_random_child_node(self):
        random_key = self.get_random_child_key()
        random_child = self.children[random_key]
        return random_child

    def calculate_winner(self, player_hands):
        for player_num in range(0, len(player_hands)):
            pass
        
    
# strategy where player chooses random move/bet
def strategy_random(node):
    return node.get_random_child_node()
                
# strategy where player chooses move that minimizes CFR
def strategy_mcts(node, valid_bets):
    pass
