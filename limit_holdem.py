from deck import *

# all values 
BIG_BLIND    = 2
LITTLE_BLIND = 1
CHECK        = 0
FOLD         = -1

class Player:

    def __init__(self):
        self.hand        = None
        self.folded      = False
        self.loser       = False
        self.checked     = False
        self.bet         = 0

# the game works like this
# each time an action is made, the game phase transitions to the next phase, and the next acting player is set.
# if 'draw' is in the game phase, the current phase is expecting a card
# if 'betting' is in the game phase, the current phase is expecting a bet from the current acting player
class Limit_Holdem:

    def __init__(self, num_players):
        self.num_players   = num_players
        self.players       = [Player() for i in range(0, self.num_players)]
        
        self.pot           = 0
        self.contribution  = 0 # current value all players need to contribute/have contibuted
        self.num_bets      = 0
        
        self.deck          = Deck()
        
        self.game_phase = 'preflop'
        
        self.flop = []
        self.turn  = None
        self.river  = None

        self.bet_counter = 0

        self.game_complete = False
        
    # deal the hands. Make players pay the blinds.
    def deal_hands(self):        
        for player_num in range(0, self.num_players):
            # each hand is a tuple of 2 cards
            self.players.hand = (self.deck.draw(), self.deck.draw())

    # get the hand of a specific player
    def get_hand(self, player_num):
        return self.players[player_num].hand
            
    def deal_community(self):
        num_community = len(self.community_cards)

        # deal flop
        if(self.game_phase == 'preflop'):
            self.flop = [self.deck.draw(), self.deck.draw(), self.deck.draw()]
            self.flop = sort_cards(self.flop)

            self.game_phase = 'flop'
            
        # deal turn 
        elif(self.game_phase == 'turn'):
            self.turn = self.deck.draw()
            self.game_phase = 'turn'
            
        # deal river
        elif(self.game_phase == 'turn'):
            self.river = self.deck.draw()
            self.game_phase = 'river'
        elif(self.game_phase == 'river'):
            self.game_complete = True
            self.calculate_winner()
        else:
            print('Error dealing cards, unexpected game phase of: ' + self.game_phase)

    # calculate the winner of the game. Find the rank and highcard of each players hand. The player with the highest rank wins. If two players tie in rank, player with the high card wins. If the high card ties, the game is a tie
    def calculate_winner(self):
        player_hand_ranks = []
        player_highcards  = []
        public_cards = self.flop + [self.turn] + [self.river]

        for player in self.players:
            if(player.folded):
                player_hand_ranks.append(FOLD)
                player_highcards.append(None)
            else:
                rank, highcard = get_hand_rank(player.hand, public_cards)
                player_hand_ranks.append(rank)
                player_highcards.append(highcard)

        winning_hand_rank = max(player_hand_ranks)
        
        
    def check(self, player_num):
        self.players[player_num].checked = True

    def uncheck_all(self):
        for player in self.players:
            player.checked = False

    def raise_bet(self, player_num, raise_size):
        pass

    # bet size is -1 for fold, 0 for check, and either 2 or 4
    # first, calculate to total players contribution to the pot for the game.
    # then, see if this contribution is equal to the current contribution
    # if greater, see if the increase (raise amount) is valid (i.e. 1 big blind), and that no more than 4 bets have been made this round. If it is, increment the bet counter
    # 
    def place_bet(self, player_num, bet_size):
        self.players[player_num].bet += bet_size

        # player folds
        if(bet_size == FOLD):
            self.players[player_num].folded = True
        #player checks
        elif(bet_size = CHECK):
            if(self.players[player_num].bet != self.contribution):
                print("Player attempted to check when player has not met the current contribution")
                exit(0)
            self.players[player_num].checked = True
        # player matches bet
        elif( (self.players[player_num].bet + bet_size) == self.contribution ):
            self.players[player_num].checked = True            
        # player raises
        elif( (self.players[player_num].bet + bet_size) > self.contribution ):
            if(self.bet_counter > 4):
                print("Attempted to bet when 4 bets have already been made")
                exit(0)
                
            raise_amount = self.players[player_num].bet - self.contribution
            if(raise_amount != BIG_BLIND):
                print("Bet attempt was too high, attempted to raise ", raise_amount)
                exit(0)

            self.players[player_num].bet += bet_size
            self.contribution += raise_amount
            self.bet_counter += 1
            self.uncheck_all()
            self.players[player_num].checked = True
            
        else:
            print("Bet attempted it was illegal, something went wrong")
            print("player num: ", player_num)
            print("bet_size: ", bet_size)
            print("game phase: ", self.game_phase)
            exit(0)

        if( (self.bet_counter == 4) and (self.all_have_checked() == True) ):
            self.bet_counter = 0
            self.uncheck_all()
            self.deal_community()



    # returns true if all remaining players have checked
    def all_have_checked(self):
        for player in self.players:
            if( (player.checked == False) and (player.folded == False) ):
                return False
        return True


    # hand ranks listed 0-8:
    # 0: high card
    # 1: one pair
    # 2: two pair
    # 3: three of a kind
    # 4: straight
    # 5: flush
    # 6: full house
    # 7: four of a kind
    # 8: straight flush
    def get_hand_rank(self, hand, public_cards):
        all_cards = hand + public_cards

        sorted_cards = sort_cards(all_cards)

        straight_flush, high_card_rank = self.is_straight_flush(hand[:], public_cards[:])
        if(straight_flush):
            return 8, high_card_rank

        four_of_a_kind, high_card_rank = self.is_four_of_a_kind(sorted_cards[:])
        if(four_of_a_kind):
            return 7, high_card_rank

        full_house, high_card_rank = self.is_full_house(sorted_cards[:])
        if(full_house):
            return 6, high_card_rank

        flush, high_card_rank = self.is_flush(hand[:], public_cards[:])
        if(flush):
            return 5, high_card_rank

        straight, high_card_rank = self.is_straight(sorted_cards[:])
        if(straight):
            return 4, high_card_rank

        three_of_a_kind, high_card_rank = self.is_three_of_a_kind(sorted_cards[:])
        if(three_of_a_kind):
            return 3, high_card_rank

        two_pair, high_card_rank = self.is_two_pair(sorted_cards[:])
        if(two_pair):
            return 2, high_card_rank

        pair, high_card_rank = self.is_pair(sorted_cards[:])
        if(pair):
            return 1, high_card_rank

        return 0, self.get_high_card(hand[:])


    def get_high_card(self, cards):
        max_rank = cards[0].rank

        if(max_rank == ACE_LOW):
            return ACE_LOW

        for card in cards:
            if(card.rank > max_rank):
                max_rank = card.rank

        return max_rank

    def is_straight_flush(self, hand, public):

        all_cards = hand + public

        if(len(all_cards) < 5):
            return False, None

        suit_counter = [[] for i in range(0, NUM_SUITS)]
        flush_suit = None
        high_card_rank = None

        # first discover if a flush exists.
        for card in all_cards:
            suit_counter[card.suit].append(card)
            if(len(suit_counter[card.suit]) == 5):
                flush_suit = card.suit

        if(flush_suit == None):
            return False, None

        sorted_flush_cards = sort_cards(suit_counter[flush_suit])

        consecutive_counter = 1
        consecutive_cards = [sorted_flush_cards[0]]
        high_card_rank = None

        # duplicate all aces to be high and low
        for card in sorted_flush_cards:
            if(card.rank == 0):
                sorted_flush_cards.append(Card(card.suit, ACE_HIGH))

        # then, discover if the flush is also a straight
        for i in range(1, len(sorted_flush_cards)):
            if(sorted_flush_cards[i].rank == sorted_flush_cards[i-1].rank + 1):
                consecutive_counter += 1
                consecutive_cards.append(sorted_flush_cards[i])
            elif(sorted_flush_cards[i].rank == sorted_flush_cards[i-1].rank):
                consecutive_cards.append(sorted_flush_cards[i])
            else:
                consecutive_counter = 1
                consecutive_cards = []

            if(consecutive_counter >= 5):
                high_card_rank = sorted_flush_cards[i].rank


        if(high_card_rank != None):
            if(high_card_rank == ACE_HIGH):
                return True, ACE_LOW
            else:
                return True, high_card_rank

        return False, None

    # returns True if a four of a kind is present. False if not.
    def is_four_of_a_kind(self, sorted_cards):
        if(len(sorted_cards) < 4):
           return False

        for i in range(0, len(sorted_cards) - 3):
            if(sorted_cards[i].rank == sorted_cards[i+1].rank == sorted_cards[i+2].rank == sorted_cards[i+3].rank):
                return True, sorted_cards[i].rank

        return False, None

    # determine if a deck is a full house. First, determine if a 3 of a kinds is present. If it is, delete the cards from the list. Then determine if a pair exists.
    def is_full_house(self, sorted_cards):
        if(len(sorted_cards) < 5):
            return False, None    

        three_of_a_kind = False
        three_of_a_kind_rank = None
        pair_rank = None

        for i in range(0, len(sorted_cards) - 2):
            if(sorted_cards[i].rank == sorted_cards[i+1].rank == sorted_cards[i+2].rank):
                three_of_a_kind = True
                three_of_a_kind_rank = sorted_cards[i].rank
                sorted_cards[i:i+2] = []
                break

        pair, pair_rank = self.is_pair(sorted_cards)

        if(three_of_a_kind and pair):
            if(three_of_a_kind_rank == ACE_LOW or pair_rank == ACE_LOW):
                return True, ACE_LOW
            elif(three_of_a_kind_rank > pair_rank):
                return True, three_of_a_kind_rank
            else:
                return True, pair_rank

        return False, None


    # returns True if a TOAK is present. False if not.
    def is_three_of_a_kind(self, sorted_cards):    
        if(len(sorted_cards) < 3):
            return False, None

        three_of_a_kind_rank = None
        # iterate over all the cards. If two three of a kinds are present, it will get the rank of the higher TOAK
        for i in range(0, len(sorted_cards) - 2):
            if(sorted_cards[i].rank == sorted_cards[i+1].rank == sorted_cards[i+2].rank):
                # if TOAK is of rank ace, that is the highest possible rank.
                if(sorted_cards[i].rank == ACE_LOW):
                    return True, ACE_LOW
                three_of_a_kind_rank = sorted_cards[i].rank

        if(three_of_a_kind_rank != None):
            return True, three_of_a_kind_rank
        else:
            return False, None

    # returns True if a pair is present, along with rank of card if a pair is present. False if not. 
    def is_pair(self, sorted_cards):
        if(len(sorted_cards) < 2):
            return False, None

        pair_rank = None

        for i in range(0, len(sorted_cards) - 1):
            if(sorted_cards[i].rank == sorted_cards[i+1].rank):
                if(pair_rank == None):
                    pair_rank = sorted_cards[i].rank
                elif(sorted_cards[i].rank > pair_rank):
                    pair_rank = sorted_cards[i].rank

        if(pair_rank != None):
            return True, pair_rank
        else:
            return False, None

    # returns True if a pair is present. False if not.
    # determines the rank of the first pair. If a pair of a different rank exists, a two pair exists
    # returns True if a pair is present. False if not.
    def is_two_pair(self, sorted_cards):
        if(len(sorted_cards) < 4):
            return False, None

        pairs_found = 0

        rank_of_high_pair = None

        for i in range(0, len(sorted_cards) - 1):
            if(sorted_cards[i].rank == sorted_cards[i+1].rank):
                pairs_found += 1            
                if(rank_of_high_pair == None):
                    rank_of_high_pair = sorted_cards[i].rank
                elif((sorted_cards[i].rank > rank_of_high_pair) and (rank_of_high_pair != ACE_LOW)):
                    rank_of_high_pair = sorted_cards[i].rank


        if(pairs_found >= 2):
            return True, rank_of_high_pair
        else:
            return False, None


    # detemine if a hand is a flush
    # count all the cards of each suit. If one of the counts is 5 or above, the hand is a flush
    # returns: None if no flush is present.
    #          An integer corresponding to the suit of the flush if there is a flush
    def is_flush(self, hand, public_cards):

        all_cards = hand + public_cards

        if(len(all_cards) < 5):
            return False, None

        suit_counter = [0 for i in range(0, NUM_SUITS)]
        flush_suit = None
        high_card_rank = None

        for card in all_cards:
            suit_counter[card.suit] += 1
            if(suit_counter[card.suit] == 5):
                flush_suit = card.suit

        # find the high card of flush in the players hand if a flush exists. This is the high card of the player in a tie scenario
        if(flush_suit != None):
            for card in hand:
                if(card.suit == flush_suit):
                    # if an ace is in the flush, that's the high card
                    if(card.rank == 0):
                        return True, card.rank

                    if(high_card_rank == None):
                        high_card_rank = card.rank
                    elif(card.rank > high_card_rank):
                        high_card_rank = card.rank

        if(flush_suit != None):
            return True, high_card_rank
        else:
            return False, None

    def is_straight(self, sorted_cards):
        if(len(sorted_cards) < 5):
            return False, None

        # duplicate all aces to be high and low
        for card in sorted_cards:
            if(card.rank == 0):
                sorted_cards.append(Card(card.suit, ACE_HIGH))

        consecutive_counter = 1
        previous_val = sorted_cards[0].rank
        high_card_rank = None

        for card in sorted_cards[1:]:
            if(card.rank == previous_val + 1):
                consecutive_counter += 1
            elif(card.rank == previous_val):
                pass
            else:
                consecutive_counter = 1
            # since the card list is sorted, each subsequent card that continues the straight is gauranteed to be of a higher rank
            if(consecutive_counter >= 5):
                high_card_rank = card.rank

            previous_val = card.rank

        if(high_card_rank != None):
            if(high_card_rank == ACE_HIGH):
                return True, ACE_LOW
            else:
                return True, high_card_rank
        else:
            return False, None
