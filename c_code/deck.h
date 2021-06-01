#ifndef DECK_H
#define DECK_H

#include <iostream>
#include <stdint.h>
#include <vector>
#include <algorithm>    // std::random_shuffle
#include <ctime>        // std::time
#include <cstdlib>      // std::rand, std::srand
#include <iterator>
#include <initializer_list>

#include "types.h"

class Card
{
public:
  card_suit_t suit;
  card_rank_t rank;

  // default constructor
  Card()
  {
    Card::suit = 0;
    Card::rank = 0;
  }
  
  Card(card_suit_t suit, card_rank_t rank)
  {
    Card::suit = suit;
    Card::rank = rank;
  }
  
  bool operator< (const Card &other) const
  {
    if(suit < other.suit)
    {
      return true;
    }
    if((suit == other.suit) && (rank < other.rank))
    {
      return true;
    }
    return false;
  }

  bool operator> (const Card &other) const
  {
    if(suit > other.suit)
    {
      return true;
    }
    if((suit == other.suit) && (rank > other.rank))
    {
      return true;
    }
    return false;
  }
};

class Deck
{
public:
  uint32_t deck_counter;
  Card deck[DECK_SIZE];

  // default constructor
  Deck()
  {
    deck_counter = 0;
    
    for(card_rank_t rank = 0; rank < NUM_RANKS; rank++)
    {
      for(card_suit_t suit = 0; suit < NUM_SUITS; suit++)
      {
	deck[deck_counter].suit = suit;
	deck[deck_counter].rank = rank;
	deck_counter++;
      }
    }
    
    deck_counter = 0;
  }

  Card draw();
  void shuffle();
};

void print_card_list(Card * list, uint32_t list_size);
void sort_card_list(Card * card_list, uint32_t list_len);
bool card_cmp(Card card1, Card card2);

#endif // DECK_H
