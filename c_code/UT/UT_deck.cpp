#include "UT_deck.h"
#include "../deck.h"
#include <vector>

void card_class_UT()
{
  bool success = true;

  Card card1, card2, card3, card4;
  card1.rank = 0;
  card1.suit = 0;

  card2.rank = 10;
  card2.suit = 0;

  card3.rank = 0;
  card3.suit = 1;

  card4.rank = 5;
  card4.suit = 1;

  if(card2 < card1)
  {
    std::cout << "card_class_UT failure: card2 less than card1\n";
    success = false;
  }
  if(card3 < card1)
  {
    std::cout << "card_class_UT failure: card3 less than card1\n";
    success = false;
  }
  if(card4 < card1)
  {
    std::cout << "card_class_UT failure: card4 less than card1\n";
    success = false;
  }
  if(card3 < card2)
  {
    std::cout << "card_class_UT failure: card3 less than card2\n";
    success = false;
  }
  if(card4 < card2)
  {
    std::cout << "card_class_UT failure: card4 less than card2\n";
    success = false;
  }
  if(card4 < card3)
  {
    std::cout << "card_class_UT failure: card4 less than card3\n";
    success = false;
  }
  

  if(card1 > card2)
  {
    std::cout << "card_class_UT failure: card1 greater than card2\n";
    success = false;
  }
  if(card1 > card3)
  {
    std::cout << "card_class_UT failure: card1 greater than card3\n";
    success = false;
  }
  if(card1 > card4)
  {
    std::cout << "card_class_UT failure: card1 greater than card4\n";
    success = false;
  }
  if(card2 > card3)
  {
    std::cout << "card_class_UT failure: card2 greater than card3\n";
    success = false;
  }
  if(card2 > card4)
  {
    std::cout << "card_class_UT failure: card2 greater than card4\n";
    success = false;
  }
  if(card3 > card4)
  {
    std::cout << "card_class_UT failure: card3 greater than card4\n";
    success = false;
  }

  
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

    if(current_card.suit > next_card.suit)
    {
      std::cout <<"Failure in sort_cards_UT: current card rank: " << current_card.suit << ", next card rank: " << next_card.suit << "\n";
      success = false;
    }
    else if( (current_card.rank > next_card.rank) && (current_card.suit == next_card.suit) )
    {
      std::cout <<"Failure in sort_cards_UT: current card rank: " << current_card.rank << ", next card rank: " << next_card.rank << "\n";
      success = false;
    }
  }

  if(success == true)
  {
    std::cout <<"sort_cards_UT PASSED\n";  
  }
  else
  {
    for(uint32_t i = 0; i < num_cards; i++)
    {
      std::cout << "Rank: " << cards[i].rank << "; Suit: " << cards[i].suit << "\n";
    }
    std::cout <<"sort_cards_UT FAILED\n";
  }
}

void deck_UT()
{  
  card_class_UT();
  deck_class_UT();
  sort_cards_UT();
}

