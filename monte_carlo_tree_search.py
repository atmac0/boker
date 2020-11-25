from math import *

class Node:
    # args: history            - array of all nodes to get to this node
    #       exploration_weight - integer marking the exploratin weight
    #       players_in_game    - list of booleans marking all players left in the game. Each index corresponds to a player, each boolean marks if they are still in the game
    #       acting_player      - integer marking the current acting player, used to index players_in_game. If acting player is -1, then the player is the dealer
    #       betting_round      - boolean describing if it is a betting round or not (betting round player chooses, non betting round dealer deals)
    def __init__(self, history, exploration_weight, players_in_game):
        self.history = history
        self.exploration_weight = exploration_weight
        self.players_in_game = players_in_game
        self.acting_player = self.find_acting_player()
        
        # positive CRF is a good decision. negative CFR is a bad decision
        self.avg_CFR = 0
        self.visits = 0
        self.children = dict()


    def get_parent(self):
        if(history is None):
            return None
        
        return self.history[-1]

    # find current acting player by counting up from the previous acting player until you hit the next player still in the game
    def find_acting_player(self):
        player_counter = self.get_parent().acting_player

        num_total_players = len(self.players_in_game)
        
        while(player_counter < (num_total_players * 3)):
            player_counter += 1
            if(self.players_in_game[player_counter % num_total_players] == True):
                return player_counter

        raise Exception("COULD NOT FIND ACTING PLAYER, SOMETHING WENT WRONG!")
            
    # calculate all valid bets based on the history
    def calculate_valid_bets(self):
        pass

    # calculate all cards that can be drawn based on the history
    def calculate_valid_draws(self):
        pass
        
    # args: valid_bets - a list of integers of all valid bets
    def do_rollout(self):
        self.visits += 1

        if(self.betting_round):
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
    
