from math import *
import random
import itertools
from deck import *

import pdb

EXPLORATION_WEIGHT = sqrt(2)
DEALER_PLAYER = -1


class Node:
    # args: history            - array of all nodes to get to this node
    #       exploration_weight - integer marking the exploratin weight
    #       players_in_game    - list of booleans marking all players left in the game. Each index corresponds to a player, each boolean marks if they are still in the game
    #       acting_player      - integer marking the current acting player, used to index players_in_game. If acting player is -1, then the player is the dealer
    #       betting_round      - boolean describing if it is a betting round or not (betting round player chooses, non betting round dealer deals)
    def __init__(self, history):
        self.history = history
        self.acting_player = None
        
        # positive CRF is a good decision. negative CFR is a bad decision
        self.avg_CFR = 0
        self.visits = 0
        self.children = None

    # TODO Make these functions make children using itertools. Somehow determine the cards remaining
    
    def make_children_betting(self, holdem):
        self.acting_player = holdem.acting_player
        self.children = dict()
        valid_bets = holdem.calculate_valid_bets(for_children=True)
        
        new_history = self.history.copy()
        new_history.append(self)
        
        for bet in valid_bets:
            self.children[bet] = Node(new_history)

    def make_children_dealer_private(self, holdem):
        self.children = dict()
        self.acting_player = DEALER_PLAYER
        
        new_history = self.history.copy()
        new_history.append(self)

        deck_remaining = Deck(shuffle=False).deck
        
        for pair in itertools.combinations(deck_remaining, 2):
            pair_string = card_list_to_string(pair)
            self.children[pair_string] = Node(new_history)
        
    def make_children_dealer_flop(self, holdem, player_num):
        self.children = dict()
        self.acting_player = DEALER_PLAYER
        
        new_history = self.history.copy()
        new_history.append(self)

        deck_remaining = Deck(shuffle=False).deck

        player_hand = holdem.players[player_num].hand

        # delete cards in hand of player from cards remaining
        for deck_card in reversed(deck_remaining):
            for player_card in player_hand:
                if( same_card(deck_card, player_card) ):
                    deck_remaining.remove(deck_card)
                    
        for trio in itertools.combinations(deck_remaining, 3):
            trio_string = card_list_to_string(trio)
            self.children[trio_string] = Node(new_history)
    
    def make_children_dealer_turn_river(self, holdem, player_num):
        self.children = dict()
        self.acting_player = DEALER_PLAYER
        
        new_history = self.history.copy()
        new_history.append(self)

        deck_remaining = Deck(shuffle=False).deck

        player_cards = list(holdem.players[player_num].hand)
        if(holdem.game_phase == 'river'):
            player_cards.append(holdem.turn)

        # delete cards in hand of player from cards remaining
        for deck_card in deck_remaining.copy():
            for player_card in player_cards:
                if( same_card(deck_card, player_card) ):
                    deck_remaining.remove(deck_card)

        for card in deck_remaining:
            card_string = card.to_string()
            self.children[card_string] = Node(new_history)

    
def strategy_dealer(node, holdem, player_num):
    print("traversing dealer nodes for player ", player_num)
    if(node.children == None):
        if(holdem.game_phase == 'preflop'):
            print("dealing children preflop")
            node.make_children_dealer_private(holdem)
        if(holdem.game_phase == 'flop'):
            print("dealing children flop")
            node.make_children_dealer_flop(holdem, player_num)
        if(holdem.game_phase == 'turn' or holdem.game_phase == 'river'):
            print("dealing children turn or river")
            node.make_children_dealer_turn_river(holdem, player_num)
            
    if(holdem.game_phase == 'preflop'):
        print("dealing preflop")
        card_token = card_list_to_string(holdem.players[player_num].hand)
    if(holdem.game_phase == 'flop'):
        print("dealing flop")
        card_token = card_list_to_string(holdem.flop)
    if(holdem.game_phase == 'turn'):
        print("dealing turn")
        card_token = card_list_to_string([holdem.turn])
    if(holdem.game_phase == 'river'):
        print("dealing river")
        card_token = card_list_to_string([holdem.river])

    chosen_node = node.children[card_token]
            
    return chosen_node


# strategy where player chooses max allowed bet.
def strategy_maximum_bet(player_nodes, holdem):
    
    valid_bets = holdem.calculate_valid_bets()
    player_hand_string = card_list_to_string(list(holdem.players[holdem.acting_player].hand))
    public_cards_string = card_list_to_string(holdem.get_public_card_list())
    
    print("AI playing strategy maximum bet")
    print("The valid bets are: ", valid_bets)   
    print("The AI's hand is: ", player_hand_string)
    print("The public cards are: ", public_cards_string)
    
    choice = max(valid_bets)

    print("The AI has chosen: ", choice)       

    init_children_betting(player_nodes, holdem)
    update_player_nodes(player_nodes, choice)
    holdem.place_bet(choice)


# strategy where player chooses random move/bet. Cannot choose a bet that exceeds current cash in hand
def strategy_random_bet_no_fold(player_nodes, holdem):
    
    valid_bets = holdem.calculate_valid_bets()
    player_hand_string = card_list_to_string(list(holdem.players[holdem.acting_player].hand))
    public_cards_string = card_list_to_string(holdem.get_public_card_list())
    
    #print("AI playing strategy random")
    #print("The valid bets are: ", valid_bets)   
    #print("The AI's hand is: ", player_hand_string)
    #print("The public cards are: ", public_cards_string)

    valid_bets.remove(-1) # remove fold
    
    choice = random.choice(valid_bets)

    #print("The AI has chosen: ", choice)       

    init_children_betting(player_nodes, holdem)
    update_player_nodes(player_nodes, choice)
    holdem.place_bet(choice)
    
# strategy where player chooses random move/bet. Cannot choose a bet that exceeds current cash in hand
def strategy_random_bet(player_nodes, holdem):
    
    valid_bets = holdem.calculate_valid_bets()
    player_hand_string = card_list_to_string(list(holdem.players[holdem.acting_player].hand))
    public_cards_string = card_list_to_string(holdem.get_public_card_list())
    
    print("AI playing strategy random")
    print("The valid bets are: ", valid_bets)   
    print("The AI's hand is: ", player_hand_string)
    print("The public cards are: ", public_cards_string)
    
    choice = random.choice(valid_bets)

    print("The AI has chosen: ", choice)       

    init_children_betting(player_nodes, holdem)
    update_player_nodes(player_nodes, choice)
    holdem.place_bet(choice)
    
                
# strategy where player chooses move that minimizes CFR
def strategy_mcts(node, valid_bets):
        print("Playing strategy MCTS when it hasn't been implemented!")
        exit(0)

    
        choice = None
        UCB1_of_choice = None

        # for all children, calculate the UCB1. Return the child with the largest UCB1
        for child in node.children:
            if(child.visits == 0):
                return child
            
            UCB1 = child.avg_CFR/child.visits + EXPLORATION_WEIGHT * sqrt( log(node.visits) / child.visits)

            if(choice == None):
                choice = child
                UCB1_of_choice = UCB1
            elif(UCB1 > UCB1_of_choice):
                choice = child
                UCB1_of_choice = UCB1
                
        return choice    


# get an input from the user for the next choice
def strategy_user_input(player_nodes, holdem):
    valid_bets = holdem.calculate_valid_bets()
    cash_stack = holdem.players[holdem.acting_player].cash    

    player_hand_string = card_list_to_string(list(holdem.players[holdem.acting_player].hand))
    public_cards_string = card_list_to_string(holdem.get_public_card_list())
    
    print("User playing")
    print("Please enter a valid bet. The bets available are: ", valid_bets)
    print("You have a cash stack of ", cash_stack)
    print("The current pot is ", holdem.pot)
    print("Your hand is: ", player_hand_string)
    print("The public cards are: ", public_cards_string)
    
    user_input = int(input("Bet: "))

    while(user_input not in valid_bets):
        user_input = int(input("Invalid choice: "))

    init_children_betting(player_nodes, holdem)
    update_player_nodes(player_nodes, user_input)
    holdem.place_bet(user_input)

def update_player_nodes(player_nodes, key):
    for i in range(0, len(player_nodes)):
        player_nodes[i] = player_nodes[i].children[key]

def init_children_betting(player_nodes, holdem):
    for node in player_nodes:
        node.acting_player = holdem.acting_player
        if(node.children == None):
            node.make_children_betting(holdem)
