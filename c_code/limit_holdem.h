#ifndef LIMIT_HOLDEM_H
#define LIMIT_HOLDEM_H

#include <iostream>
#include <algorithm>    // std::random_shuffle
#include <vector>       // std::vector
#include <ctime>        // std::time
#include <cstdlib>      // std::rand, std::srand

#include "deck.h"

// bet values
#define BIG_BLIND     2
#define LITTLE_BLIND  1
#define CHECK         0
#define FOLD         -1

// hand rank values
#define RANK_STRAIGHT_FLUSH   8
#define RANK_FOUR_OF_A_KIND   7
#define RANK_FULL_HOUSE       6
#define RANK_FLUSH            5
#define RANK_STRAIGHT         4
#define RANK_THREE_OF_A_KIND  3
#define RANK_TWO_PAIR         2
#define RANK_PAIR             1
#define RANK_HIGH_CARD        0

#define PREFLOP 0
#define FLOP    1
#define TURN    2
#define RIVER   3

#define NUM_PLAYERS 2

#define HAND_SIZE 2
#define FLOP_SIZE 3
#define COMMUNITY_SIZE 5
#define ALL_CARDS_SIZE 7

#define TURN_COMMUNITY_POSITION 3
#define RIVER_COMMUNITY_POSITION 4

#define UNINITIALIZED 0xDEADBEEF

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
  int32_t player_num;

  Player()
  { 
    folded = false;
    winner = false;
    checked = false;
    bet = 0;
    cash = 50 * BIG_BLIND;
    number = UNINITIALIZED;   
  }
  
  Player(uint32_t player_num)
  {
    folded = false;
    winner = false;
    checked = false;
    bet = 0;
    cash = 50 * BIG_BLIND;
    number = player_num;
  }
};

class Limit_Holdem
{
public:
  Player players[NUM_PLAYERS];
  uint32_t acting_player;
  uint32_t players_remaining;

  uint32_t pot;
  uint32_t contribution; // current value all players need to contribute/have contibuted

  Deck deck;

  uint32_t game_phase;

  Card community_cards[COMMUNITY_SIZE];
  uint32_t community_counter; // num cards dealt to the community
  
  uint32_t bet_counter;

  bool game_complete;
  bool ended_in_tie;

  Limit_Holdem()
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

    deck.shuffle();
  }

  void deal_hands();
  void deal_community();
  void calculate_winner();
  void set_winner(uint32_t * winning_players, uint32_t num_winners);
  void check(uint32_t player_num);
  void uncheck_all();
  uint32_t get_next_acting_player();
  std::vector<uint32_t> get_valid_bets();
  void place_bet(uint32_t bet);
  void end_the_game();
  void goto_next_game_phase();
  bool all_have_checked();

  uint32_t get_hand_rank(Card * private_cards, Card * public_cards);

  bool is_straight_flush(Card * private_cards, Card * public_cards, uint32_t * high_card);
  bool is_four_of_a_kind(Card * sorted_cards, uint32_t * high_card);
  bool is_full_house(Card * sorted_cards, uint32_t * high_card);
  bool is_flush(Card * private_cards, Card * public_cards, uint32_t * high_card);
  bool is_straight(Card * sorted_cards, uint32_t * high_card);
  bool is_three_of_a_kind(Card * sorted_cards, uint32_t * high_card);
  bool is_two_pair(Card * sorted_cards, uint32_t * high_card);
  bool is_pair(Card * sorted_cards, uint32_t * high_card);
  uint32_t get_high_card_rank(Card * card_list, uint32_t list_size);  
  
};

#endif // LIMIT_HOLDEM_H
