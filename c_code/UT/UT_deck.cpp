#include "UT_deck.h"
#include "../deck.h"
#include <vector>

void card_class_UT()
{
  bool success = true;

  for(uint32_t i = 0; i < NUM_RANKS; i++)
  {
    for(uint32_t j = 0; j < NUM_SUITS; j++)
    {
      Card test_card = Card(j, i);

      if(test_card.rank != i)
      {
	std::cout << "card_class_UT failure: expected rank of " << i << ", " << test_card.rank << " observed.\n";
	success = false;
      }
      if(test_card.suit != j)
      {
	std::cout << "card_class_UT failure: expected rank of " << j << ", " << test_card.suit << " observed.\n";
	success = false;
      }
    }
  }

  if(success == true)
  {
    std::cout <<"card_class_UT PASS\n";
  }
  else
  {
    std::cout <<"card_class_UT FAIL\n";
  }
}

void deck_class_UT()
{
    std::cout <<"deck_class_UT SKIPPED\n";  
}

void sort_cards_UT()
{
  bool success = true;

  uint32_t num_cards = 9;
  
  Card cards[num_cards];

  cards[0] = Card(3,5);
  cards[1] = Card(2,5);
  cards[2] = Card(1,13);
  cards[3] = Card(3,4);
  cards[4] = Card(2,12);
  cards[5] = Card(3,0);
  cards[6] = Card(2,0);
  cards[7] = Card(1,0);
  cards[8] = Card(0,0);

  sort_card_list(cards, num_cards);

  Card current_card, next_card;
  
  for(uint32_t i = 0; i < num_cards - 1; i++)
  {
    current_card = cards[i];
    next_card = cards[i+1];

    if(current_card.rank > next_card.rank)
    {
      std::cout <<"Failure in sort_cards_UT: current card rank: " << current_card.rank << ", next card rank: " << next_card.rank << "\n";
      success = false;
    }

    if(current_card.rank == next_card.rank)
    {
      if(current_card.suit > next_card.suit)
      {
	std::cout <<"Failure in sort_cards_UT: current card suit: " << current_card.suit << ", next card suit: " << next_card.suit << "\n";
	success = false;
      }
    }
  }

  if(success == true)
  {
    std::cout <<"sort_cards_UT PASSED\n";  
  }
  else
  {
    std::cout <<"sort_cards_UT FAILED\n";  
  }
}

void deck_UT()
{  
  card_class_UT();
  deck_class_UT();
  sort_cards_UT();
}

