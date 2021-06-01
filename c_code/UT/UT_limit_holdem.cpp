#include "UT_limit_holdem.h"

void constructor_UT()
{
  Limit_Holdem holdem = Limit_Holdem();

  std::cout << "limit holdem constructor_UT PASSED\n";
}

void get_hand_rank_UT()
{
  bool success = true;

  hand_rank_t hand_rank;
  card_rank_t high_card;

  Limit_Holdem holdem = Limit_Holdem();

  Card straight_flush_hand_list[2]   = {Card(0,3), Card(0,4)};
  Card straight_flush_public_list[5] = {Card(0,5), Card(0,6), Card(0,7), Card(2,12), Card(0,3)};
  card_rank_t straight_flush_high_card = 7

  Card four_of_a_kind_hand_list[2]   = {Card(0,3), Card(1,3)};
  Card four_of_a_kind_public_list[5] = {Card(2,3), Card(2,12), Card(3,7), Card(2,12), Card(0,3)};
   
  Card full_house_hand_list[2]   = {Card(0,0), Card(1,0)};
  Card full_house_public_list[5] = {Card(2,0), Card(2,12), Card(3,7), Card(2,12), Card(0,3)};
  
  Card flush_hand_list[2]   = {Card(0,2), Card(3,0)};
  Card flush_public_list[5] = {Card(2,0), Card(0,4), Card(0,3),  Card(0,2), Card(0,1)};
  
  Card straight_hand_list[2]   = {Card(0,0), Card(1,0)};
  Card straight_public_list[5] = {Card(2,4), Card(2,3), Card(3,2), Card(2,2), Card(0,1)};

  Card three_of_a_kind_hand_list[2] = {Card(0,3), Card(1,0)};
  Card three_of_a_kind_public_list[5] = {Card(2,2), Card(2,3), Card(3,7), Card(2,6), Card(1,3)};
  
  Card two_pair_hand_list[2]   = {Card(0,0), Card(1,0)};
  Card two_pair_public_list[5] = {Card(2,2), Card(2,12), Card(3,7), Card(2,7), Card(0,3)};

  Card one_pair_hand_list[2]   = {Card(0,0), Card(1,0)};
  Card one_pair_public_list[5] = {Card(2,2), Card(2,12), Card(3,7), Card(2,6), Card(0,3)};
  
  Card high_card_hand_list[2]   = {Card(0,0), Card(1,2)};
  Card high_card_public_list[7] = {Card(2,4), Card(3,6), Card(3,8), Card(2,10), Card(1,12)};

  hand_rank = holdem.get_hand_rank(straight_flush_hand_list, straight_flush_public_list, &high_card);
  if( (hand_rank != RANK_STAIGHT_FLUSH) || (high_card != straight_flush_high_card) )
  {
    	std::cout << "get_hand_rank_UT failure: expected hand rank of " << RANK_STRAIGHT_FLUSH << ", " << hand_rank << " observed.\n";
	std::cout << "high card of " << straight_flush_high_card << " expected, " << high_card << " observed.\n";
	success = false;
  }

  hand_rank = holdem.get_hand_rank(, &high_card);
  if(hand_rank != RANK_FLUSH)
  {
    	std::cout << "get_hand_rank_UT failure: expected hand rank of " << RANK_FLUSH << ", " << hand_rank << " observed.\n";
	success = false;
  }

    hand_rank = holdem.get_hand_rank(flush_hand_list, flush_public_list, &high_card);
  if(hand_rank != RANK_FLUSH)
  {
    	std::cout << "get_hand_rank_UT failure: expected hand rank of " << RANK_FLUSH << ", " << hand_rank << " observed.\n";
	success = false;
  }

    hand_rank = holdem.get_hand_rank(flush_hand_list, flush_public_list, &high_card);
  if(hand_rank != RANK_FLUSH)
  {
    	std::cout << "get_hand_rank_UT failure: expected hand rank of " << RANK_FLUSH << ", " << hand_rank << " observed.\n";
	success = false;
  }

    hand_rank = holdem.get_hand_rank(flush_hand_list, flush_public_list, &high_card);
  if(hand_rank != RANK_FLUSH)
  {
    	std::cout << "get_hand_rank_UT failure: expected hand rank of " << RANK_FLUSH << ", " << hand_rank << " observed.\n";
	success = false;
  }

    hand_rank = holdem.get_hand_rank(flush_hand_list, flush_public_list, &high_card);
  if(hand_rank != RANK_FLUSH)
  {
    	std::cout << "get_hand_rank_UT failure: expected hand rank of " << RANK_FLUSH << ", " << hand_rank << " observed.\n";
	success = false;
  }

    hand_rank = holdem.get_hand_rank(flush_hand_list, flush_public_list, &high_card);
  if(hand_rank != RANK_FLUSH)
  {
    	std::cout << "get_hand_rank_UT failure: expected hand rank of " << RANK_FLUSH << ", " << hand_rank << " observed.\n";
	success = false;
  }
  
  hand_rank = holdem.get_hand_rank(flush_hand_list, flush_public_list, &high_card);
  if(hand_rank != RANK_FLUSH)
  {
    	std::cout << "get_hand_rank_UT failure: expected hand rank of " << RANK_FLUSH << ", " << hand_rank << " observed.\n";
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
void limit_holdem_UT()
{
  constructor_UT();
  
  get_hand_rank_UT();
  is_straight_flush_UT();
  is_four_of_a_kind_UT();
  is_full_house_UT();
  is_three_of_a_kind_UT();
  is_pair_UT();
  is_two_pair_UT();
  is_flush_UT();
  is_straight_UT();
}

