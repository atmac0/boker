#include <iostream>

#include "limit_holdem.h"
#include "deck.h"
#include "types.h"

int main()
{
  std::cout << "Welcome to the terminal version of limit holdem!\n";

  uint32_t players_remaining = NUM_PLAYERS;
  
  bet_t cash_stacks[NUM_PLAYERS];

  for(uint32_t i = 0; i < NUM_PLAYERS; i++)
  {
    cash_stacks[i] = 50 * BIG_BLIND;
  }

  bool one_player_left = false;
  uint32_t non_zero_cashstack_counter = 0;
  bool valid_bet_entry = false;
  
  while(!one_player_left)
  {

    std::cout << "\n\n---- NEW GAME ----\n\n";
    
    Limit_Holdem holdem = Limit_Holdem(cash_stacks, players_remaining);

    while(holdem.game_complete == false)
    {
  
      std::cout << "Acting player is: " << holdem.acting_player << "\n";
      std::cout << "Players remaining are: " << holdem.players_remaining << "\n";
      std::cout << "Game phase is: " << holdem.game_phase << "\n";

      std::cout << "The community cards are:\n";

      for(uint32_t i = 0; i < holdem.community_counter; i++)
      {
	std::cout << "Suit: " << holdem.community_cards[i].suit << "; Rank: " << holdem.community_cards[i].rank << "\n";
      }
    
      for(uint32_t i = 0; i < holdem.players_remaining; i++)
      {
	Card * hand = holdem.players[i].hand;

	std::cout << "Player " << i << " starting stats:\n";

	std::cout << "Hand:\n";
	for(uint32_t j = 0; j < HAND_SIZE; j++)
	{
	  Card current_card = hand[j];
	  std::cout << "Suit: " << current_card.suit << "; Rank: " << current_card.rank << "\n";
	}

	std::cout << "Cash stack: " << holdem.players[i].cash << "\n";
	std::cout << "Current bet size: " << holdem.players[i].bet << "\n";
      }

      std::vector<bet_t> valid_bets = holdem.calculate_valid_bets(false);

      std::cout << "The pot is: " << holdem.pot << "\n";

      std::cout << "The current contribution is: " << holdem.contribution << "\n";
    
      std::cout << "Valid bets for acting player " << holdem.acting_player << ":\n";
      
      for(bet_t i : valid_bets)
      {
	std::cout << i << "\n";
      }


      valid_bet_entry = false;
      bet_t user_bet;
      
      while(!valid_bet_entry)
      {
	std::cout << "Please type a bet to place: ";

	std::cin >> user_bet;

	for(bet_t i: valid_bets)
	{
	  if(user_bet == i)
	  {
	    valid_bet_entry = true;
	  }
	}
      }

      holdem.place_bet(user_bet);
      
    }
    
    for(uint32_t i = 0; i < NUM_PLAYERS; i++)
    {
      if(holdem.players[i].winner)
      {
	std::cout << "Player " << i << " won!\n";
      }
      else
      {
	std::cout << "Player " << i << " lost\n";
      }
    }

    if(holdem.ended_in_tie)
    {
      std::cout << "Game ended in tie\n";
    }


    non_zero_cashstack_counter = 0;
    for(uint32_t i = 0; i < players_remaining; i++)
    {
      cash_stacks[i] = holdem.players[i].cash;
       
      if(holdem.players[i].cash > 0)
      {
	non_zero_cashstack_counter++;
      }
    }

    if(non_zero_cashstack_counter == 1)
    {
      one_player_left = true;
    }
    
  }
  
  return 0;
}
