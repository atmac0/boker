#include <vector>
#include <iostream>

#include "deck.h"

void print_card_list(Card * list, uint32_t list_size)
{

  std::cout << "PRINTING DECK\n";
  
  for(uint32_t i = 0; i < list_size; i++)
  {
    std::cout << "Deck suit/rank: " << list[i].suit << " " << list[i].rank << "\n" ;
  }
}

/* 
@param: card_list - an array of cards
@param: list_len  - len of card list
@brief: sort cards high to low. This list will be a maximum size of 7 cards will be sorted by rank first, then suit; e.g. 2 of hearts is greater than 6 of clubs. However 7 of diamonds is greater than 7 of spades this uses bubble sort. This could definitely be improved
@post:
*/
void sort_card_list(Card * card_list, uint32_t list_len)
{
  std::sort(card_list, card_list + list_len);
}

/*
@param: card1
@param: card2
@brief: compare two cards
@return: true if the cards are the same. False it not.
*/
bool card_cmp(Card card1, Card card2)
{
  if(card1.rank == card2.rank)
  {
    if(card1.suit == card2.suit)
    {
      return true;
    }
  }
  return false;
}


Card Deck::draw()
{
  Card drawn_card = deck[deck_counter];
  deck_counter++;
  return drawn_card;
}

void Deck::shuffle()
{
  std::random_shuffle(deck, deck + DECK_SIZE);
}
