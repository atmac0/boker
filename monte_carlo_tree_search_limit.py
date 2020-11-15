from math import *
from itertools import *

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
    def __init__(self, history, exploration_weight, players_in_game):
        self.history               = history
        self.exploration_weight    = exploration_weight
        self.players_in_game       = players_in_game
        self.acting_player         = self.find_acting_player()
        
        if(bet_made != None):
            self.bet_made          = bet_made
            self.betting_node      = True
            # remove current acting player from the game if they folded
            if(self.bet_made == -1):
                self.players_in_game[self.acting_player] =  False
        else:
            assert card_drawn is not None
            self.card_drawn    = card_drawn
            self.betting_node  = False

        self.num_players_in_game = get_num_players_in_game()
        
        # positive CRF is a good decision. negative CFR is a bad decision
        self.avg_CFR = 0
        self.visits = 0

        self.children = None

        self.current_round_string = self.get_current_round()
        self.next_round_string    = self.get_next_round_string()


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
        next_round_string = self.get_next_round_string()
        
        if('betting' in next_round_string):
            self.make_children_betting()
        elif('draw' in next_round_string):
            self.make_children_drawing()
        else:
            raise Exception('ERROR IN MAKING CHILDREN. ILLEGAL CHILD: ' + next_round_string)

    def get_children(self):
        if(self.children is None):
            self.make_children()

        return self.children

    def make_children_betting(self):
        self.children = dict()
        next_round_string = self.get_next_round_string()
        valid_bets = self.calculate_valid_bets()

        for(bet in valid_bets):
            next_history = self.history.append(self)

            if(bet == -1):
                next_players_in_game = self.players_in_game.copy()
                next_players_in_game[self.acting_player] = False
                self.children[str(bet)] = Node(next_history, self.exploration_weight, next_players_in_game, 
            
            self.children[str(bet)] = Node(next_history, self
        

        
    def make_children_drawing(self):
        self.children = dict()
        remaining_deck = self.calculate_valid_draws()

        for card in remaining_deck:
            card_string = card.to_string()

            next_history = self.history.append(self)
            self.children[card_string] = Node(next_history, self.exploration_weight, self.players_in_game)
        
    def next_acting_player(self):
        player_counter = self.acting_player

        num_total_players = len(self.players_in_game)

        # exit condition should only be satisfied in the case of an error
        while(player_counter < (num_total_players * 3) ):
            player_counter += 1
            if(self.players_in_game[player_counter % num_total_players] == True):
                return player_counter


        raise Exception("COULD NOT FIND NEXT ACTING PLAYER, SOMETHING WENT WRONG!")

                
    def bets_since_draw(self):
        nodes_in_round = []
                
        for node in reversed(self.history):
            if(node.betting_round = False):
                break
            nodes_in_round.append(node)

        if(nodes_in_round > 4):
            raise Exception('ERROR: NUMBER OF BETS SINCE DRAW EXCEEDED EXPECTED NUMBER OF 4')
            
        return nodes_in_round

    def num_bets_since_draw(self):
        return len(self.bets_since_draw())
    
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
        if
    
    # determine the next round
    # returns: 'pre_flop_betting'
    #          'flop_draw'
    #          'flop_betting'
    #          'turn_draw'
    #          'turn_betting'
    #          'river_draw'
    #          'river_betting'
    #          'terminal'
    # first determine if the flop has been completed. If not, the next round is a drawing round.
    # then, determine if all players have matched their previous raises.
    # then, detemine if betting is over. There is up to 1 bet, and 3 raises for each round.
    # returns terminal if the current node is a terminal node
    def get_next_round_string(self):

        if(self.num_players_in_game == 1):
            return 'terminal'
        
        num_cards_drawn = self.num_cards_drawn()  
        num_bets_since_draw = self.bets_since_draw()
        is_betting_over = self.did_all_players_match_bet()

        if(1 <= num_cards_drawn < 3):
            return 'flop_draw'
        
        if(is_betting_over):
            if(self.current_round_string == 'pre_flop_betting'):
                return 'flop_draw'
            elif(self.current_round_string == 'flop_betting'):
                return 'turn_draw'
            elif(self.current_round_string == 'turn_betting'):
                return 'river_draw'
            else:
                return 'terminal'
        
        if(num_bets_since_draw < 4):
            return self.current_round_string

        raise Exception("ERROR CALCULATING NEXT ROUND. REACHED END OF FUNCTION")
    
        
    # determine the current round
    # returns: "pre_flop_betting"
    #          "flop_draw"
    #          "flop_betting"
    #          "turn_draw"
    #          "turn_betting"
    #          "river_draw"
    #          "river_betting"
    def get_current_round(self):
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
        
    
    # calculate all valid bets based on the history. This will be some multiple of the big blind
    def calculate_valid_bets(self):
        pass
        
        
        # get just the betting history for this round. If a player has folded this round, they are no longer in the round, and should not be included for betting.
        nodes_in_round = []
        for node in reversed(self.history):
            if(node.betting_round = False):
                break
            if(self.players_in_game[node.acting_player]):
                nodes_in_round.append(node)


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
        bets_in_round = self.bets_since_draw()

        # if all the players (counting from the start of the round) have yet to have an action, the round cannot be over
        if(len(bets_in_round) < bets_in_round[0].num_players_in_game):
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
        bets_in_round = self.bets_since_draw()
        bet_sums = dict()
        
        for bet in bets_in_round:
            bet_sums[str(bet.acting_player)] += bet.bet_made

        return bet_sums
        
        
            
        
        
    # calculate if the next round is a betting round
    # this is done by adding up all the bets of all acting players in the round, if all values are equal
    # if 
    def is_next_round_betting(self):

        num_cards_drawn = self.num_cards_drawn()
        current_round = self.current_round_string()

        # if current round is turn or river draw, the next round must be betting
        if( current_round == 'turn_draw' or current_round == 'river_draw' ):
            return True
        # if the current round is part of the flop, but not all cards have been draw, the next round must be a draw round
        if( current_round == 'flop_draw' and num_cards_drawn < 3 ):
            return False
                       
        bets_in_round = self.bets_since_draw()
        
        player_bets = [0 for i in self.players_in_games]
        for node in notes_in_round
            if(self.players 
            player_bets[node.acting_player] = node.bet_made
               
               
            
        for player_boolean in players_in_game:
            if not player_boolean:
    
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
                                        

class MCTS:

    def __init__(self, exploration_weight, layer_type):
        self.Q         = 0 # total reward of each node
        self.N         = 0 # total visit count for each node
        self.layer_type = layer_type # layer type, used for computing children
        self.visits    = 0

        self.game_state = {0:"betting1", 1:"preflop", 2:"betting2", 3:"turn", 4:"betting3", 5:"river", 6:"betting4"}

        do_rollout()


    def do_rollout(layer):
        if(self.game_state["betting1"] == self.layer_type):
            decisions = [1,10,100,1000] # placeholder bet amounts
            regret = []
        elif(self.game_state["preflop"] == self.layer_type):
            pass
        elif(self.game_state["betting2"] == self.layer_type):
            pass
        elif(self.game_state["turn"] == self.layer_type):
            pass
        elif(self.game_state["betting3"] == self.layer_type):
            pass
        elif(self.game_state["river"] == self.layer_type):
            pass
        elif(self.game_state["betting4"] == self.layer_type):
            pass        


# strategy where player chooses random move/bet
def strategy_random(node, valid_bets):
    pass
                
# strategy where player chooses move that minimizes CFR
def strategy_mcts(node, valid_bets):
    pass
