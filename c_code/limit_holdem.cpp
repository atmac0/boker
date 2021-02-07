#include "limit_holdem.h"


void Limit_Holdem::deal_hands()
{
  for(uint32_t player_num = 0; player_num < NUM_PLAYERS; player_num++)
  {
    for(uint32_t hand_counter = 0; hand_counter < HAND_SIZE; hand_counter++)
    {
      players[player_num].hand[hand_counter] = deck.draw();
    }
  }
}

void Limit_Holdem::deal_community()
{
  if(game_phase == PREFLOP)
  {
    // deal flop
    for(uint32_t i = 0; i < FLOP_SIZE; i++)
    {
      community_cards[i] = deck.draw();
    }
    sort_card_list(community_cards, FLOP_SIZE); // sort the flop
    game_phase = FLOP;
  }
  else if(game_phase == FLOP) // deal turn
  {
    community_cards[TURN_COMMUNITY_POSITION] = deck.draw();
    game_phase = TURN;
  }
  else if(game_phase == TURN) // deal river
  {
    community_cards[RIVER_COMMUNITY_POSITION] = deck.draw();
    game_phase = RIVER;
  }
  else
  {
    std::cout << "ERROR: dealing cards, unexpected game phase of " << game_phase << "\n";
    std::exit(1);
  }
}

void Limit_Holdem::calculate_winner()
{
  int32_t winning_player_rank = UNINITIALIZED;
  int32_t winning_player_high_card = UNINITIALIZED;
  int32_t winning_players[NUM_PLAYERS] = {UNINITIALIZED};
  uint32_t rank, highcard;

  for(uint32_t player_num = 0; player_num < NUM_PLAYERS; player_num++)
  {
    player = players[player_num];

    if(!player.folded)
    {
      rank = get_hand_rank(player.hand, community_cards, &highcard);
    }
  }
}

void Limit_Holdem::set_winner(uint32_t * winning_players, uint32_t num_winners)
{
  for(uint32_t player_num = 0; player_num < NUM_PLAYERS; player_num++)
  {
    // if player is a winner
    if(std::find(winning_players, winning_players + num_winners, player_num))
    {
      players[player_num].winner = true;
    }
    else
    {
      players[player_num].winner = false;
    }
  }
}

void Limit_Holdem::check(uint32_t player_num)
{
  players[player_num].checked = true;
}

void Limit_Holdem::uncheck_all()
{
  for(uint32_t player_num = 0; player_num < NUM_PLAYERS; player_num++)
  {
    players[player_num].checked = false;
  }
}

uint32_t Limit_Holdem::get_next_acting_player()
{
  // search from the current player up
  for(uint32_t player_num = acting_player; player_num < NUM_PLAYERS; player_num++)
  {
    Player player = players[player_num];
    if(player.player_num == acting_player)
    {
      // skip
    }
    else if(player.folded == false)
    {
      return player.number
    }
  }

  // search from the first player to the current player
  for(uint32_t player_num = acting_player; player_num < NUM_PLAYERS; player_num++)
  {
    Player player = players[player_num];
    if(player.number == acting_player)
    {
      //pass
    }
    else if(player.folded == False)
    {
      return player.number
    }
  }

  std::cout << "ERROR: Could not increment acting player, no unfolded player other than the current acting player found!\n";
  std::exit(1);
}

std::vector<uint32_t> Limit_Holdem::get_valid_bets();
void Limit_Holdem::place_bet(uint32_t bet);
void Limit_Holdem::end_the_game();

void Limit_Holdem::goto_next_game_phase()
{
  if(game_phase == RIVER)
  {
    end_the_game();
  }
  else
  {
    bet_counter = 0;
    uncheck_all();
    deal_community();
  }
}

bool Limit_Holdem::all_have_checked()
{
  for(uint32_t player_num = 0; player_num < NUM_PLAYERS; player_num++)
  {
    if( (players[player_num].checked == false) && (players[player_num].folded == false) )
    {
      return false;
    }
  }
  return true;
}


uint32_t Limit_Holdem::get_hand_rank(Card * private_cards, Card * public_cards, uint32_t * high_card);

bool Limit_Holdem::is_straight_flush(Card * private_cards, Card * public_cards, uint32_t * high_card);
bool Limit_Holdem::is_four_of_a_kind(Card * sorted_cards, uint32_t * high_card);
bool Limit_Holdem::is_full_house(Card * sorted_cards, uint32_t * high_card);
bool Limit_Holdem::is_flush(Card * private_cards, Card * public_cards, uint32_t * high_card);
bool Limit_Holdem::is_straight(Card * sorted_cards, uint32_t * high_card);
bool Limit_Holdem::is_three_of_a_kind(Card * sorted_cards, uint32_t * high_card);
bool Limit_Holdem::is_two_pair(Card * sorted_cards, uint32_t * high_card);
bool Limit_Holdem::is_pair(Card * sorted_cards, uint32_t * high_card);
uint32_t Limit_Holdem::get_high_card_rank(Card * card_list, uint32_t list_size);


