#ifndef TYPES_H
#define TYPES_H

typedef unsigned int  uint32_t;
typedef unsigned long uint64_t;

typedef int  int32_t;
typedef long int64_t;

typedef int32_t  card_suit_t;
typedef int32_t  card_rank_t;
typedef int32_t  player_num_t;

typedef int32_t  bet_t;

typedef uint32_t hand_rank_t;

// bet values
#define BIG_BLIND     2
#define LITTLE_BLIND  1
#define CHECK         0
#define FOLD         -1

// hand rank values
#define RANK_STRAIGHT_FLUSH   8
#define RANK_FOUR_OF_A_KIND   7
#define RANK_FULL_HOUSE       6
#define RANK_FLUSH            5
#define RANK_STRAIGHT         4
#define RANK_THREE_OF_A_KIND  3
#define RANK_TWO_PAIR         2
#define RANK_PAIR             1
#define RANK_HIGH_CARD        0
#define RANK_NONE            -1

#define PREFLOP 0
#define FLOP    1
#define TURN    2
#define RIVER   3

#define NUM_PLAYERS 2

#define HAND_SIZE 2
#define FLOP_SIZE 3
#define COMMUNITY_SIZE 5
#define ALL_CARDS_SIZE 7

#define TURN_COMMUNITY_POSITION 3
#define RIVER_COMMUNITY_POSITION 4


#define DECK_SIZE 52

#define NUM_SUITS 4
#define NUM_RANKS 13

#define NO_SUIT  -1
#define SPADE     0
#define CLUB      1
#define DIAMONDS  2
#define HEARTS    3

#define ACE_LOW   0
#define ONE       1
#define TWO       2
#define THREE     3
#define FOUR      4
#define FIVE      5
#define SIX       6
#define SEVEN     7
#define EIGHT     8
#define NINE      9
#define TEN       10
#define JACK      11
#define QUEEN     12
#define KING      13
#define ACE_HIGH  14

#define UNINITIALIZED 0xDEADBEEF

#endif // TYPES_H

