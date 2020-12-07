from math import *
from monte_carlo_tree_search_limit import *
from deck import *

little_blind = 2
big_blind = 4

has_bet = False
raise_count = 0




def main():
    player_count = 2
    players_in_game = [True for i in range(0, player_count)]
    
    exploration_weight = sqrt(2)
    node_head = Node([], exploration_weight, players_in_game, None)

    # list of tree positions for all players
    player_nodes = [node_head for i in range(0, player_count)]

    deck = Deck()

    # loop forever
    while(True):

        holdem = Limit_Holdem(player_count)
        
        # loop while the game is still ongoing
        while(not holdem.game_complete):
            if(current_node.acting_player == -1):
                print("DEALER PLAYING")
                card = deck.draw()
                current_node = strategy_dealer(current_node, card)
            # all other players will play with a random strategy for testing. This will eventually be changed to a MCTS
            elif(current_node.acting_player != 0):
                print("USER PLAYING")
                current_node = strategy_random(current_node, cash_stacks)
            else:
                print("RANDOM PLAYING")
                current_node = strategy_user_input(current_node, cash_stacks)


        print("GAME ENDED, RESTARTING")
        current_node = node_head

if(__name__ == "__main__"):
    main()
