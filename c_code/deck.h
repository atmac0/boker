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

const uint32_t DECK_SIZE = 52;

const uint32_t NUM_SUITS = 4;
const uint32_t NUM_RANKS = 14;

const uint32_t NO_SUIT  = -1;
const uint32_t SPADE    = 0;
const uint32_t CLUB     = 1;
const uint32_t DIAMONDS = 2;
const uint32_t HEARTS   = 3;

const uint32_t ACE_LOW  = 0;
const uint32_t ONE      = 1;
const uint32_t TWO      = 2;
const uint32_t THREE    = 3;
const uint32_t FOUR     = 4;
const uint32_t FIVE     = 5;
const uint32_t SIX      = 6;
const uint32_t SEVEN    = 7;
const uint32_t EIGHT    = 8;
const uint32_t NINE     = 9;
const uint32_t TEN      = 10;
const uint32_t JACK     = 11;
const uint32_t QUEEN    = 12;
const uint32_t KING     = 13;
const uint32_t ACE_HIGH = 14;


class Card
{
public:
  uint32_t suit;
  uint32_t rank;

  // default constructor
  Card()
  {
    Card::suit = 0;
    Card::rank = 0;
  }
  
  Card(uint32_t suit, uint32_t rank)
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
    if(rank < other.rank)
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
    
    for(uint32_t rank = 0; rank < NUM_RANKS; rank++)
    {
      for(uint32_t suit = 0; suit < NUM_SUITS; suit++)
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
