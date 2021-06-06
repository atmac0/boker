#include "UT_limit_holdem.h"

void get_hand_rank_UT()
{
  bool success = true;

  hand_rank_t hand_rank;
  card_rank_t high_card;

  Limit_Holdem holdem = Limit_Holdem();

  Card straight_flush_hand_list[2]   = {Card(0,3), Card(0,4)};
  Card straight_flush_public_list[5] = {Card(0,5), Card(0,6), Card(0,7), Card(2,12), Card(0,3)};
  card_rank_t straight_flush_high_card = 7;

  Card four_of_a_kind_hand_list[2]   = {Card(0,3), Card(1,3)};
  Card four_of_a_kind_public_list[5] = {Card(2,3), Card(2,12), Card(3,7), Card(1,12), Card(3,3)};
  card_rank_t four_of_a_kind_high_card = 3;
  
  Card full_house_hand_list[2]   = {Card(0,0), Card(1,0)};
  Card full_house_public_list[5] = {Card(2,0), Card(2,12), Card(3,7), Card(2,12), Card(0,3)};
  card_rank_t full_house_high_card = 0;
  
  Card flush_hand_list[2]   = {Card(0,2), Card(3,0)};
  Card flush_public_list[5] = {Card(2,0), Card(0,4), Card(0,3),  Card(0,2), Card(0,1)};
  card_rank_t flush_high_card = 2;
  
  
  Card straight_hand_list[2]   = {Card(0,0), Card(1,0)};
  Card straight_public_list[5] = {Card(2,4), Card(2,3), Card(3,2), Card(2,2), Card(0,1)};
  card_rank_t straight_high_card = 4;

  Card three_of_a_kind_hand_list[2] = {Card(0,3), Card(1,0)};
  Card three_of_a_kind_public_list[5] = {Card(2,2), Card(2,3), Card(3,7), Card(2,6), Card(1,3)};
  card_rank_t three_of_a_kind_high_card = 3;
  
  Card two_pair_hand_list[2]   = {Card(0,0), Card(1,0)};
  Card two_pair_public_list[5] = {Card(2,2), Card(2,12), Card(3,7), Card(2,7), Card(0,3)};
  card_rank_t two_pair_high_card = 0;
  
  Card one_pair_hand_list[2]   = {Card(0,0), Card(1,0)};
  Card one_pair_public_list[5] = {Card(2,2), Card(2,12), Card(3,7), Card(2,6), Card(0,3)};
  card_rank_t  one_pair_high_card = 0;
  
  Card high_card_hand_list[2]   = {Card(0,0), Card(1,2)};
  Card high_card_public_list[7] = {Card(2,4), Card(3,6), Card(3,8), Card(2,10), Card(1,12)};
  card_rank_t high_card_high_card = 0;
  
  hand_rank = holdem.get_hand_rank(straight_flush_hand_list, straight_flush_public_list, &high_card);
  if( hand_rank != RANK_STRAIGHT_FLUSH )
  {
    std::cout << "get_hand_rank_UT failure: straight flush: expected hand rank of " << RANK_STRAIGHT_FLUSH << ", " << hand_rank << " observed.\n";
    success = false;
  }
  if( high_card != straight_flush_high_card )
  {
    std::cout << "get_hand_rank_UT failure: straight flsuh: expected high card of " << straight_flush_high_card << ", " << high_card << " observed.\n";
    success = false;
  }

  hand_rank = holdem.get_hand_rank(four_of_a_kind_hand_list, four_of_a_kind_public_list, &high_card);
  if( hand_rank != RANK_FOUR_OF_A_KIND )
  {
    	std::cout << "get_hand_rank_UT failure: four of a kind: expected hand rank of " << RANK_FOUR_OF_A_KIND << ", " << hand_rank << " observed.\n";
	success = false;
  }
  if( high_card != four_of_a_kind_high_card )
  {
    std::cout << "get_hand_rank_UT failure: four of a kind: expected high card of " << four_of_a_kind_high_card << ", " << high_card << " observed.\n";
    success = false;
  }  

  hand_rank = holdem.get_hand_rank(full_house_hand_list, full_house_public_list, &high_card);
  if( hand_rank != RANK_FULL_HOUSE )
  {
    	std::cout << "get_hand_rank_UT failure: full house: expected hand rank of " << RANK_FULL_HOUSE << ", " << hand_rank << " observed.\n";
	success = false;
  }
  if( high_card != full_house_high_card )
  {
    std::cout << "get_hand_rank_UT failure: full house: expected high card of " << full_house_high_card << ", " << high_card << " observed.\n";
    success = false;
  }  

  hand_rank = holdem.get_hand_rank(flush_hand_list, flush_public_list, &high_card);
  if( hand_rank != RANK_FLUSH )
  {
    	std::cout << "get_hand_rank_UT failure: flush: expected hand rank of " << RANK_FLUSH << ", " << hand_rank << " observed.\n";
	success = false;
  }
  if( high_card != flush_high_card )
  {
    std::cout << "get_hand_rank_UT failure: flush: expected high card of " << flush_high_card << ", " << high_card << " observed.\n";
    success = false;
  }  

  hand_rank = holdem.get_hand_rank(straight_hand_list, straight_public_list, &high_card);
  if( hand_rank != RANK_STRAIGHT )
  {
    	std::cout << "get_hand_rank_UT failure: straight: expected hand rank of " << RANK_STRAIGHT << ", " << hand_rank << " observed.\n";
	success = false;
  }
  if( high_card != straight_high_card )
  {
    std::cout << "get_hand_rank_UT failure: straight: expected high card of " << straight_high_card << ", " << high_card << " observed.\n";
    success = false;
  }

  hand_rank = holdem.get_hand_rank(three_of_a_kind_hand_list, three_of_a_kind_public_list, &high_card);
  if( hand_rank != RANK_THREE_OF_A_KIND )
  {
    	std::cout << "get_hand_rank_UT failure: three of a kind: expected hand rank of " << RANK_THREE_OF_A_KIND << ", " << hand_rank << " observed.\n";
	success = false;
  }
  if( high_card != three_of_a_kind_high_card )
  {
    std::cout << "get_hand_rank_UT failure: three of a kind: expected high card of " << three_of_a_kind_high_card << ", " << high_card << " observed.\n";
    success = false;
  }

  hand_rank = holdem.get_hand_rank(two_pair_hand_list, two_pair_public_list, &high_card);
  if( hand_rank != RANK_TWO_PAIR )
  {
    	std::cout << "get_hand_rank_UT failure: two pair: expected hand rank of " << RANK_TWO_PAIR << ", " << hand_rank << " observed.\n";
	success = false;
  }
  if( high_card != two_pair_high_card )
  {
    std::cout << "get_hand_rank_UT failure: two pair: expected high card of " << two_pair_high_card << ", " << high_card << " observed.\n";
    success = false;
  }

  hand_rank = holdem.get_hand_rank(one_pair_hand_list, one_pair_public_list, &high_card);
  if( hand_rank != RANK_PAIR )
  {
    	std::cout << "get_hand_rank_UT failure: one pair: expected hand rank of " << RANK_PAIR << ", " << hand_rank << " observed.\n";
	success = false;
  }
  if( high_card != one_pair_high_card )
  {
    std::cout << "get_hand_rank_UT failure: one pair: expected high card of " << one_pair_high_card << ", " << high_card << " observed.\n";
    success = false;
  }

  hand_rank = holdem.get_hand_rank(high_card_hand_list, high_card_public_list, &high_card);
  if( hand_rank != RANK_HIGH_CARD )
  {
    	std::cout << "get_hand_rank_UT failure: high card: expected hand rank of " << RANK_HIGH_CARD << ", " << hand_rank << " observed.\n";
	success = false;
  }
  if( high_card != high_card_high_card )
  {
    std::cout << "get_hand_rank_UT failure: high card: expected high card of " << high_card_high_card << ", " << high_card << " observed.\n";
    success = false;
  }  
  
  
  if(success == true)
  {
    std::cout <<"get_hand_rank_UT PASSED\n";
  }
  else
  {
    std::cout <<"get_hand_rank_UT FAILED\n";
  }
}
void is_straight_flush_UT()
{
  
}
void is_four_of_a_kind_UT()
{

}
void is_full_house_UT()
{

}
void is_three_of_a_kind_UT()
{

}
void is_pair_UT()
{

}
void is_two_pair_UT()
{

}
void is_flush_UT()
{

}
void is_straight_UT()
{

}

void get_all_cards_sorted_UT()
{
  Card private_cards[] = {Card(0,3), Card(1,3)};
  Card public_cards[]  = {Card(2,3), Card(2,12), Card(3,7), Card(1,12), Card(3,3)};
  
  Limit_Holdem holdem = Limit_Holdem();

  Card * sorted_cards = holdem.get_all_cards_sorted(private_cards, public_cards);

  bool success = true;
  
  for(uint32_t i = 0; i < ALL_CARDS_SIZE - 1; i++)
  {
    Card card1 = sorted_cards[i];
    Card card2 = sorted_cards[i + 1];
    
    if(card1.rank > card2.rank)
    {
      std::cout << "get_all_cards_sorted_UT failure: card at index " << i << " has suit of " << card1.suit << ", next card has suit of " << card2.suit << "\n";
      success = false;
    }
    if(card1.rank == card2.rank)
    {
      if(card1.suit > card2.suit)
      {
      std::cout << "get_all_cards_sorted_UT failure: card at index " << i << " has rank of " << card1.rank << ", next card has rank of " << card2.rank << "\n";
      success = false;
      }
    }
  }

  if(success == true)
  {
    std::cout <<"get_all_cards_sorted_UT PASSED\n";
  }
  else
  {
    for(uint32_t i = 0; i < ALL_CARDS_SIZE; i++)
    {
      std::cout << "SUIT: " << sorted_cards[i].suit << " RANK: " << sorted_cards[i].rank << "\n";
    }
    
    std::cout <<"get_all_cards_sorted_UT FAILED\n";
  }
}

void limit_holdem_UT()
{  
  get_hand_rank_UT();
  is_straight_flush_UT();
  is_four_of_a_kind_UT();
  is_full_house_UT();
  is_three_of_a_kind_UT();
  is_pair_UT();
  is_two_pair_UT();
  is_flush_UT();
  is_straight_UT();
  get_all_cards_sorted_UT();
}

