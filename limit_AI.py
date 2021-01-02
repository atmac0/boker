from math import *
from monte_carlo_tree_search import *
from deck import *
from limit_holdem import *

import pdb

def main():
    # variables needed to initialize and keep track of game/MCST    
    player_count = 2
    exploration_weight = sqrt(2)
    node_head = Node([]) # head node players will reset to at end of game
    
    # list of current tree positions for all players
    player_nodes = [node_head for i in range(0, player_count)]

    num_games_played = 0
    num_games_won    = 0
    
    # Play limit texas holdem, loop forever
    while(True):
        print("Welcome to Limit Texas holdem with {0} players!".format(player_count))

        # start a new game
        holdem = Limit_Holdem(player_count)
        game_phase = holdem.game_phase
        
        # deal the private information set for each player
        for player_num in range(0, player_count):
            player_nodes[player_num] = strategy_dealer(player_nodes[player_num], holdem, player_num)
        
        # loop while the game is still ongoing
        while(not holdem.game_complete):
            
            if(game_phase != holdem.game_phase):
                game_phase = holdem.game_phase

                if(game_phase == 'flop'):
                    cards_drawn = holdem.flop
                if(game_phase == 'turn'):
                    cards_drawn = [holdem.turn]
                if(game_phase == 'river'):
                    cards_drawn = [holdem.river]

                cards_drawn_token = card_list_to_string(cards_drawn)

                for player_num in range(0, player_count):
                    node_after_draw = strategy_dealer(player_nodes[player_num], holdem, player_num)
                    player_nodes[player_num] = node_after_draw
                    
            
            # all other players will play with a random strategy for testing. This will eventually be changed to a MCTS
            elif(holdem.acting_player == 0):
                #strategy_user_input(player_nodes, holdem)
                strategy_maximum_bet(player_nodes, holdem)
            else:
                strategy_maximum_bet(player_nodes, holdem)



        print("The game has ended.")
        for player in holdem.players:
            if((player.number == 0) and (player.winner == True)):
                num_games_won += 1
            
            if(player.winner):
                print("Player {0} won".format(player.number))
            else:
                print("Player {0} lost".format(player.number))

        num_games_played += 1
        print("GAMES PLAYED: ", num_games_played)
        print("WIN RATIO: ", num_games_won/num_games_played)
        print(" ")
        print("Restarting...")
        
        player_nodes = [node_head for i in range(0, player_count)]        

if(__name__ == "__main__"):
    main()
