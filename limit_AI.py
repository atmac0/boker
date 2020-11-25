from math import *
from monte_carlo_tree_search import *

little_blind = 2
big_blind = 4

has_bet = False
raise_count = 0




def main():
    player_count = 2

    
    exploration_weight = sqrt(2)

    players_in_game = [True, True]
    node_head = Node(None, exploration_weight, players_in_game, None)
    current_node = node_head
    #players_tree_loc = [search_tree_head for i in range(0, player_count)] # tree location for each player

    deck = Deck()
    
    while(True):

        game = Limit_Holdem(player_count, big_blind, little_blind)
        
        while(game.current_round_string != 'terminal'):
            if('betting' in current_node.current_round_string):
                current_node = strategy_random(current_node)
            elif('flop_draw' == current_node.current_round_string):
                drawn_cards = [deck.draw() for i in range(0, 3)]
                
            
                
            
    


if(__name__ == "__main__"):
    main()
