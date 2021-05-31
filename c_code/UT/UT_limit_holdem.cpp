#include "UT_limit_holdem.h"

bool get_hand_rank_UT()
{
  bool success = true;

  int32_t hand_rank;
  uint32_t high_card;
  
  Limit_Holdem holdem = Limit_Holdem();

  Card straight_flush_list[7] = {Card(0,3), Card(0,4), Card(0,5), Card(0,6), Card(0,7), Card(2,12), Card(0,3)};
  Card four_of_a_kind_list[7] = {Card(0,3), Card(1,3), Card(2,3), Card(2,12), Card(3,7), Card(2,12), Card(0,3)};
  Card full_house_list[7] = {Card(0,0), Card(1,0), Card(2,0), Card(2,12), Card(3,7), Card(2,12), Card(0,3)};

  Card flush_hand_list[2] = {Card(0,2), Card(3,0)};
  Card flush_public_list[5] = {Card(2,0), Card(0,4), Card(0,3),  Card(0,2), Card(0,1)};
    
  Card straight_list[7] = {Card(0,0), Card(1,0), Card(2,4), Card(2,3), Card(3,2), Card(2,2), Card(0,1)};
  Card three_of_a_kind_list[7] = {Card(0,3), Card(1,0), Card(2,2), Card(2,3), Card(3,7), Card(2,6), Card(1,3)};
  Card two_pair_list[7] = {Card(0,0), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,7), Card(0,3)};
  Card one_pair_list[7] = {Card(0,0), Card(1,0), Card(2,2), Card(2,12), Card(3,7), Card(2,6), Card(0,3)};
  Card high_card_list[7] = {Card(0,0), Card(1,2), Card(2,4), Card(3,6), Card(3,8), Card(2,10), Card(1,12)};
  return false;
}
bool is_straight_flush_UT()
{
  return false;
}
bool is_four_of_a_kind_UT()
{
  return false;
}
bool is_full_house_UT()
{
  return false;
}
bool is_three_of_a_kind_UT()
{
  return false;
}
bool is_pair_UT()
{
  return false;
}
bool is_two_pair_UT()
{
  return false;
}
bool is_flush_UT()
{
  return false;
}
bool is_straight_UT()
{
  return false;
}
bool limit_holdem_UT()
{
  bool get_hand_rank_UT();
  bool is_straight_flush_UT();
  bool is_four_of_a_kind_UT();
  bool is_full_house_UT();
  bool is_three_of_a_kind_UT();
  bool is_pair_UT();
  bool is_two_pair_UT();
  bool is_flush_UT();
  bool is_straight_UT();
  return false;
}

