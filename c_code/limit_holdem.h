#ifndef LIMIT_HOLDEM_H
#define LIMIT_HOLDEM_H

#include <iostream>
#include <algorithm>    // std::random_shuffle
#include <vector>       // std::vector
#include <ctime>        // std::time
#include <cstdlib>      // std::rand, std::srand
#include <string>

#include "deck.h"
#include "types.h"

class Player
{
public:
  Card hand[HAND_SIZE];
  uint32_t hand_rank;
  bool folded;
  bool winner;
  bool checked;
  uint32_t bet;
  uint32_t cash;
  player_num_t number;

  Player()
  { 
    folded = false;
    winner = false;
    checked = false;
    bet = 0;
    cash = 0;
    number = UNINITIALIZED;   
  }
  
  Player(uint32_t player_num)
  {
    folded = false;
    winner = false;
    checked = false;
    bet = 0;
    cash = 0;
    number = player_num;
  }
};

class Limit_Holdem
{
public:
  Player players[NUM_PLAYERS];
  player_num_t acting_player;
  uint32_t players_remaining;

  uint32_t pot;
  uint32_t contribution; // current value all players need to contribute/have contibuted

  uint32_t game_phase;

  Card community_cards[COMMUNITY_SIZE];
  uint32_t community_counter; // num cards dealt to the community
  
  bool game_complete;
  bool ended_in_tie;
  
  void check(uint32_t player_num);

  std::vector<bet_t> calculate_valid_bets(bool for_children);
  void place_bet(bet_t bet);
  void pay_blinds();
  
  hand_rank_t get_hand_rank(Card * private_cards, Card * public_cards, card_rank_t * high_card);
  bool is_straight_flush(Card * private_cards, Card * public_cards, card_rank_t * high_card);
  bool is_four_of_a_kind(Card * sorted_cards, card_rank_t * high_card);
  bool is_full_house(Card * sorted_cards, card_rank_t * high_card);
  bool is_flush(Card * private_cards, Card * public_cards, card_rank_t * high_card);
  bool is_straight(Card * sorted_cards, card_rank_t * high_card);
  bool is_three_of_a_kind(Card * sorted_cards, card_rank_t * high_card);
  bool is_two_pair(Card * sorted_cards, card_rank_t * high_card);
  bool is_pair(Card * sorted_cards, card_rank_t * high_card);
  card_rank_t get_high_card(Card * card_list, uint32_t list_size);
  Card * get_all_cards_sorted(Card * private_cards, Card * public_cards);


  
  Limit_Holdem(bet_t * cash_stacks)
  {
    acting_player = 0;
    players_remaining = NUM_PLAYERS;

    pot = 0;
    contribution = 0;

    game_phase = PREFLOP;
    
    community_counter = 0;
    
    bet_counter = 0; // counter for the total number of bets made this round

    game_complete = false;
    ended_in_tie  = false;

    for(uint32_t i = 0; i < NUM_PLAYERS; i++)
    {
      players[i].cash = cash_stacks[i];
      players[i].number = i;
    }
    
    deck.shuffle();

    pay_blinds();
    deal_hands();
    
  }
  
private:
  void deal_hands();
  void deal_community();
  void calculate_winner();
  void set_winner(std::vector<player_num_t> winning_players);

  void uncheck_all();
  player_num_t next_acting_player();

  
  void end_the_game();
  void goto_next_game_phase();
  bool all_have_checked();
  
  uint32_t bet_counter;

  Deck deck;  
};

#endif // LIMIT_HOLDEM_H
