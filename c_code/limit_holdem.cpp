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

// calculate the winner of the game. Find the rank and highcard of each players hand. The player with the highest rank wins. If two players tie in rank, player with the high card wins. If the high card ties, the game is a tie
void Limit_Holdem::calculate_winner()
{
  int32_t winning_player_rank = RANK_NONE;
  int32_t winning_player_high_card, high_card;
  std::vector<uint32_t> winning_players;
  int32_t rank;

  for(uint32_t player_num = 0; player_num < NUM_PLAYERS; player_num++)
  {
    Player player = players[player_num];

    if(!player.folded)
    {
      rank = get_hand_rank(player.hand, community_cards, &high_card);

      // current player has a better rank than the previous highest
      if(rank > winning_player_rank)
      {
	winning_player_rank = rank;
	winning_player_high_card = high_card;
	winning_players.clear();
	winning_players.push_back(player_num);
      }
      // current player has the same rank as the previous highest
      else if(rank == winning_player_rank)
      {
	// a flush can possibly have no high card (flush is entirely made up from public cards). These conditions account for it
	// current winner and current player has flush but no high card
	if( (rank == RANK_FLUSH) && (high_card == RANK_NONE) && (winning_player_high_card == RANK_NONE) )
	{
	  winning_players.push_back(player_num);
	}
	// current player has a high card and current winner does not
	else if( (rank == RANK_FLUSH) && (high_card != RANK_NONE) && (winning_player_high_card == RANK_NONE) )
	{
	  winning_player_rank = rank;
	  winning_player_high_card = high_card;
	  winning_players.clear();
	  winning_players.push_back(player_num);
	}
	// current winner has high card and current player does not
	else if( (rank == RANK_FLUSH) && (high_card == RANK_NONE) && (winning_player_high_card != RANK_NONE) )
	{
	  // pass
	}
	// end of flush conditions. This next statement encompasses all other hands.
	else if(high_card > winning_player_high_card)
	{
	  winning_player_rank = rank;
	  winning_player_high_card = high_card;
	  winning_players.clear();
	  winning_players.push_back(player_num);	  
	}
	// if the player has a matching rank and highcard, consider them for a tie. They need to be considered as another play may also tie, or outrank them and win.
	else if(high_card == winning_player_high_card)
	{
	  winning_players.push_back(player_num);
	}
      }
    }
  }

  set_winner(winning_players);

  if(winning_players.size() > 1)
  {
    ended_in_tie = true;
  }
  
}

void Limit_Holdem::set_winner(std::vector<uint32_t> winning_players)
{
  for(uint32_t player_num = 0; player_num < NUM_PLAYERS; player_num++)
  {
    // if player is a winner
    if(std::find(winning_players.begin(), winning_players.end(), player_num) != winning_players.end())
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

uint32_t Limit_Holdem::next_acting_player()
{
  // search from the current player up
  for(int32_t player_num = acting_player; player_num < NUM_PLAYERS; player_num++)
  {
    Player player = players[player_num];
    if(player.number == acting_player)
    {
      // skip
    }
    else if(player.folded == false)
    {
      return player.number;
    }
  }

  // search from the first player to the current player
  for(int32_t player_num = acting_player; player_num < NUM_PLAYERS; player_num++)
  {
    Player player = players[player_num];
    if(player.number == acting_player)
    {
      //pass
    }
    else if(player.folded == false)
    {
      return player.number;
    }
  }

  std::cout << "ERROR: Could not increment acting player, no unfolded player other than the current acting player found!\n";
  std::exit(1);
}

/* 
calculate valid bets.
   args: for_children: determines if this is being called to calculate the valid children of a node. If it is, it will ignore the cash stack of the player, and return all bets legal by the rules of limit poker 
*/
std::vector<int32_t> Limit_Holdem::calculate_valid_bets(bool for_children)
{
  std::vector<int32_t> valid_bets;
  valid_bets.push_back(FOLD);

  Player current_player = players[acting_player];

  // player has already matched current contribution, and can thus check
  if(current_player.bet == contribution)
  {
    valid_bets.push_back(CHECK);
  }

  int64_t contribution_diff = contribution - current_player.bet;

  // player can match current contribution
  if( for_children || ((contribution_diff > 0) && ((int64_t)current_player.cash > contribution_diff)))
  {
    valid_bets.push_back(contribution_diff);
  }

  // player raises
  if(bet_counter < 4)
  {
    if( for_children || ((int64_t)current_player.cash > (contribution_diff + BIG_BLIND)))
    {
      valid_bets.push_back(contribution_diff + BIG_BLIND);
    }
  }

  return valid_bets;
}

/*
bet size is -1 for fold, 0 for check, and either 2 or 4
first, calculate to total players contribution to the pot for the game.
then, see if this contribution is equal to the current contribution
if greater, see if the increase (raise amount) is valid (i.e. 1 big blind), and that no more than 4 bets have been made this round. If it is, increment the bet counter
*/    
void Limit_Holdem::place_bet(uint32_t bet_size)
{
  Player * p_current_player = &players[acting_player];

  // player folds
  if(bet_size == FOLD)
  {
    p_current_player->folded = true;
    players_remaining--;

    if(players_remaining == 1)
    {
      game_complete = true;
      players[next_acting_player()].winner = true;
      return;
    }
  }
  // player checks
  else if(bet_size == CHECK)
  {
    if(p_current_player->bet != contribution)
    {
      std::cout << "ERROR: Player attempted to check when player has not met the current contribution\n";
      std::exit(1);
    }
    p_current_player->checked = true;
  }
  // player matches bet
  else if((p_current_player->bet + bet_size) == contribution)
  {
    p_current_player->checked  = true;
    p_current_player->cash    -= bet_size;
    p_current_player->bet     += bet_size;
    pot                       += bet_size;
  }
  // player raises
  else if( (p_current_player->bet + bet_size) > contribution )
  {
    if(bet_counter > 4)
    {
      std::cout << "ERROR: Attempted to bet when 4 bets have already been made\n";
      std::exit(1);
    }

    uint32_t raise_amount = (p_current_player->bet + bet_size) - contribution;
    if(raise_amount != BIG_BLIND)
    {
      std::cout << "ERROR: Bet attempt was too high, attempted to raise " << raise_amount << "\n";
      std::exit(1);
    }

    p_current_player->bet    += bet_size;
    p_current_player->cash   -= bet_size;
    contribution             += raise_amount;
    pot                      += bet_size;
    bet_counter++;
    uncheck_all();
    p_current_player->checked = true;
  }
  else
  {
    std::cout << "ERROR: Bet attempted was illegal, something went wrong.\n";
    std::cout << "player num : " << p_current_player->number << "\n";
    std::cout << "bet size   : " << bet_size << "\n";
    std::cout << "game phase : " << game_phase << "\n";
    std::exit(1);
  }

  acting_player = next_acting_player();

  if(all_have_checked())
  {
    goto_next_game_phase();
  }
}
void Limit_Holdem::end_the_game()
{
  game_complete = true;
  calculate_winner();
}

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

Card * Limit_Holdem::get_all_cards_sorted(Card * private_cards, Card * public_cards)
{
  static Card sorted_cards[ALL_CARDS_SIZE];

  sorted_cards[0] = private_cards[0];
  sorted_cards[1] = private_cards[1];

  sorted_cards[2] = public_cards[0];
  sorted_cards[3] = public_cards[1];
  sorted_cards[4] = public_cards[2];
  sorted_cards[5] = public_cards[3];
  sorted_cards[6] = public_cards[4];

  sort_card_list(sorted_cards, ALL_CARDS_SIZE);

  return sorted_cards;  
}

/* hand ranks listed 0-8:
   0: high card
   1: one pair
   2: two pair
   3: three of a kind
   4: straight
   5: flush
   6: full house
   7: four of a kind
   8: straight flush */
uint32_t Limit_Holdem::get_hand_rank(Card * private_cards, Card * public_cards, int32_t * high_card)
{
  Card * sorted_cards = get_all_cards_sorted(private_cards, public_cards);
  
  bool is_hand;

  *high_card = RANK_NONE;
  is_hand = is_straight_flush(private_cards, public_cards, high_card);
  if(is_hand)
  {
    return RANK_STRAIGHT_FLUSH;
  }

  *high_card = RANK_NONE;
  is_hand = is_four_of_a_kind(sorted_cards, high_card);
  if(is_hand)
  {
    return RANK_FOUR_OF_A_KIND;
  }

  *high_card = RANK_NONE;
  is_hand = is_full_house(sorted_cards, high_card);
  if(is_hand)
  {
    return RANK_FULL_HOUSE;
  }
  
  *high_card = RANK_NONE;
  is_hand = is_flush(private_cards, public_cards, high_card);
  if(is_hand)
  {
    return RANK_FLUSH;
  }

  *high_card = RANK_NONE;
  is_hand = is_straight(sorted_cards, high_card);
  if(is_hand)
  {
    return RANK_STRAIGHT;
  }

  *high_card = RANK_NONE;
  is_hand = is_three_of_a_kind(sorted_cards, high_card);
  if(is_hand)
  {
    return RANK_THREE_OF_A_KIND;
  }

  *high_card = RANK_NONE;
  is_hand = is_two_pair(sorted_cards, high_card);
  if(is_hand)
  {
    return RANK_TWO_PAIR;
  }

  *high_card = RANK_NONE;
  is_hand = is_pair(sorted_cards, high_card);
  if(is_hand)
  {
    return RANK_PAIR;
  }

  *high_card = RANK_HIGH_CARD;
  return get_high_card(sorted_cards, ALL_CARDS_SIZE);
}

bool Limit_Holdem::is_straight_flush(Card * private_cards, Card * public_cards, int32_t * high_card)
{
    Card * sorted_cards = get_all_cards_sorted(private_cards, public_cards);

    std::vector<Card> suit_counter[NUM_SUITS];
    suit_t flush_suit = SUIT_NONE;
    *high_card = RANK_NONE;

    // first discover if a flush exists
    for(uint32_t i = 0; i < ALL_CARDS_SIZE; i++)
    {
      suit_counter[sorted_cards[i].suit].push_back(sorted_cards[i]);
      if(suit_counter[sorted_cards[i].suit].size() == 5)
      {
	flush_suit = sorted_cards[i].suit;
      }
    }

    if(flush_suit == SUIT_NONE)
    {
      return false;
    }

    std::vector<Card> flush_cards = suit_counter[flush_suit];
    
    std::sort(flush_cards.begin(), flush_cards.end());
    
    uint32_t consecutive_counter = 1;
    std::vector<Card> consecutive_cards;
    consecutive_cards.push_back(flush_cards[0]);

    // duplicate all aces to be high and low
    for(Card card : flush_cards)
    {
      if(card.rank == ACE_LOW)
      {
      flush_cards.push_back(Card(card.suit, ACE_HIGH));
      }
    }

    for(uint32_t i = 1; i < flush_cards.size(); i++)
    {
      if(flush_cards.at(i).rank == (flush_cards.at(i - 1).rank + 1))
      {
	consecutive_counter += 1;
	consecutive_cards.push_back(flush_cards.at(i));
      }
      else if(flush_cards.at(i).rank == (flush_cards.at(i - 1).rank))
      {
	consecutive_cards.push_back(flush_cards.at(i));
      }
      else
      {
	consecutive_counter = 1;
	consecutive_cards.clear();
      }

      if(consecutive_counter >= 5)
      {
	*high_card = flush_cards.at(i).rank;
      }
    }

    if(*high_card != RANK_NONE)
    {
      if(*high_card == ACE_HIGH)
      {
	*high_card = ACE_LOW;
	return true;
      }
      else
      {
	return true;
      }
    }

    return false;
    
}
bool Limit_Holdem::is_four_of_a_kind(Card * sorted_cards, int32_t * high_card)
{
  for(uint32_t i = 0; i < ALL_CARDS_SIZE - 3; i++)
  {
    if((sorted_cards[i].rank == sorted_cards[i+1].rank) && (sorted_cards[i].rank == sorted_cards[i+2].rank) && (sorted_cards[i].rank == sorted_cards[i+3].rank))
    {
      *high_card = sorted_cards[i].rank;
      return true;
    }
  }

  *high_card = RANK_NONE;
  return false;
}

bool Limit_Holdem::is_full_house(Card * sorted_cards, int32_t * high_card)
{
  bool three_of_a_kind = false;
  bool pair = false;
  int32_t three_of_a_kind_rank = RANK_NONE;
  int32_t pair_rank = RANK_NONE;
  
  for(uint32_t i = 0; i < ALL_CARDS_SIZE - 2; i++)
  {
    // check if three of a kind exists
    if((sorted_cards[i].rank == sorted_cards[i+1].rank) && (sorted_cards[i].rank == sorted_cards[i+2].rank))
    {
      three_of_a_kind = true;
      three_of_a_kind_rank = sorted_cards[i].rank;
      break;
    }
  }

  for(uint32_t i = 0; i < ALL_CARDS_SIZE - 1; i++)
  {
    // check if a pair exists separate from the three of a kind
    if(sorted_cards[i].rank == sorted_cards[i+1].rank)
    {
      if(sorted_cards[i].rank != three_of_a_kind_rank)
      {
	pair = true;
	pair_rank = sorted_cards[i].rank;
      }
    }
  }

  if(three_of_a_kind && pair)
  {
    if((three_of_a_kind_rank == ACE_LOW) || (pair_rank == ACE_LOW))
    {
      *high_card = ACE_LOW;
    }
    else if(three_of_a_kind_rank > pair_rank)
    {
      *high_card = three_of_a_kind_rank;
    }
    else
    {
      *high_card = pair_rank;
    }
    return true;
  }

  *high_card = RANK_NONE;
  return false;
}

bool Limit_Holdem::is_flush(Card * private_cards, Card * public_cards, int32_t * high_card)
{
  uint32_t suit_counter[NUM_SUITS] = {0};
  int32_t  flush_suit = NO_SUIT;
  *high_card = RANK_NONE;

  /* find the cards in the flush, if one exists */
  for(uint32_t i = 0; i <  COMMUNITY_SIZE; i++)
  {
    uint32_t current_card_suit = public_cards[i].suit;
    suit_counter[current_card_suit]++;
    if(suit_counter[current_card_suit] == 5)
    {
      flush_suit = current_card_suit;
    }
  }
  for(uint32_t i = 0; i < HAND_SIZE; i++)
  {
    uint32_t current_card_suit = private_cards[i].suit;
    suit_counter[current_card_suit]++;
    if(suit_counter[current_card_suit] == 5)
    {
      flush_suit = current_card_suit;
    }
  }

  if(flush_suit != NO_SUIT)
  {
    /* find the players high card in the suit in hand, if any */
    for(uint32_t i = 0; i < HAND_SIZE; i++)
    {
      if(private_cards[i].suit == flush_suit)
      {
	/* edge case for ace high card */
	if(private_cards[i].rank == ACE_LOW)
	{
	  *high_card = ACE_LOW;
	  return true;
	}

	if(*high_card == RANK_NONE)
	{
	  *high_card = private_cards[i].rank;
	}
	else if(private_cards[i].rank > *high_card)
	{
	  *high_card = private_cards[i].rank;
	}
      }
    }
  }

  if(flush_suit != NO_SUIT)
  {
    return true;
  }
  else
  {
    return false;
  }
}

bool Limit_Holdem::is_straight(Card * sorted_cards, int32_t * high_card)
{
  uint32_t consecutive_counter = 1;
  uint32_t previous_rank = sorted_cards[0].rank;
  *high_card = RANK_NONE;
  
  for(uint32_t i = 0; i < ALL_CARDS_SIZE; i++)
  {
    if(sorted_cards[i].rank == previous_rank + 1)
    {
      consecutive_counter++;
    }
    else if(sorted_cards[i].rank == previous_rank)
    {
      /* pass */
    }
    /* account for ace being stored as 0 */
    else if( (previous_rank == KING) && (sorted_cards[0].rank == ACE_LOW) )
    {
      consecutive_counter++;
    }
    else
    {
      consecutive_counter = 1;
    }

    if(consecutive_counter >= 5)
    {
      *high_card = sorted_cards[i].rank;
    }

    previous_rank = sorted_cards[i].rank;
  }

  if(*high_card != RANK_NONE)
  {
    return true;
  }
  else
  {
    return false;
  }
}

bool Limit_Holdem::is_three_of_a_kind(Card * sorted_cards, int32_t * high_card)
{
  *high_card = RANK_NONE;
  
  for(uint32_t i = 0; i < ALL_CARDS_SIZE - 2; i++)
  {
    if( (sorted_cards[i].rank == sorted_cards[i+1].rank) && (sorted_cards[i].rank == sorted_cards[i+2].rank) )
    {
      if(sorted_cards[i].rank == ACE_LOW)
      {
	*high_card = ACE_LOW;
	return true;
      }
      *high_card = sorted_cards[i].rank;
    }
  }

  if(*high_card != RANK_NONE)
  {
    return true;
  }
  else
  {
    return false;
  }
}
bool Limit_Holdem::is_two_pair(Card * sorted_cards, int32_t * high_card)
{
  uint32_t pairs_found = 0;
  *high_card = RANK_NONE;

  for(uint32_t i = 0; i < ALL_CARDS_SIZE; i++)
  {
    if(sorted_cards[i].rank == sorted_cards[i+1].rank)
    {
      pairs_found++;
      if( (sorted_cards[i].rank > *high_card) && (*high_card != ACE_LOW) )
      {
	*high_card = sorted_cards[i].rank;
      }
    }
  }

  if(pairs_found >= 2)
  {
    return true;
  }
  else
  {
    return false;
  }
}

bool Limit_Holdem::is_pair(Card * sorted_cards, int32_t * high_card)
{
  *high_card = RANK_NONE;

  for(uint32_t i = 0; i < ALL_CARDS_SIZE; i++)
  {
    if(sorted_cards[i].rank == sorted_cards[i+1].rank)
    {
      if( (sorted_cards[i].rank > *high_card) && (*high_card != ACE_LOW) )
      {
	*high_card = sorted_cards[i].rank;
      }
    }
  }

  if(*high_card != RANK_NONE)
  {
    return true;
  }
  else
  {
    return false;
  }
}

uint32_t Limit_Holdem::get_high_card(Card * card_list, uint32_t list_size)
{
  uint32_t max_rank = card_list[0].rank;

  if(max_rank == ACE_LOW)
  {
    return ACE_LOW;
  }
  
  for(uint32_t i = 0; i < ALL_CARDS_SIZE; i++)
  {
    if(card_list[i].rank > max_rank)
    {
      max_rank = card_list[i].rank;
    }
  }

  return max_rank;
}


