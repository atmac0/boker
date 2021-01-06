from deck import *
import pdb

BIG_BLIND    = 2
LITTLE_BLIND = 1
CHECK        = 0
FOLD         = -1

# hand rank values
RANK_STRAIGHT_FLUSH  = 8
RANK_FOUR_OF_A_KIND  = 7
RANK_FULL_HOUSE      = 6
RANK_FLUSH           = 5
RANK_STRAIGHT        = 4
RANK_THREE_OF_A_KIND = 3
RANK_TWO_PAIR        = 2
RANK_PAIR            = 1
RANK_HIGH_CARD       = 0

class Player:

    def __init__(self, player_num):
        self.hand        = None
        self.hand_rank   = None
        self.folded      = False
        self.winner      = False
        self.checked     = False
        self.bet         = 0
        self.cash        = 50 * BIG_BLIND
        self.number      = player_num


# the game works like this
# each time an action is made, the game phase transitions to the next phase, and the next acting player is set.
# if 'draw' is in the game phase, the current phase is expecting a card
# if 'betting' is in the game phase, the current phase is expecting a bet from the current acting player
class Limit_Holdem:

    def __init__(self, num_players):
        self.num_players   = num_players
        self.players       = [Player(i) for i in range(0, self.num_players)]
        self.acting_player = 0
        self.players_remaining = num_players
        
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
        self.ended_in_tie  = False

        self.deal_hands()
        
    # deal the hands. Make players pay the blinds.
    def deal_hands(self):        
        for player in self.players:
            # each hand is a tuple of 2 cards
            hand = [self.deck.draw(), self.deck.draw()]
            hand = sort_cards(hand)
            player.hand = tuple(hand)
            
    def deal_community(self):
        # deal flop
        if(self.game_phase == 'preflop'):
            self.flop = sort_cards([self.deck.draw(), self.deck.draw(), self.deck.draw()])
            self.game_phase = 'flop'
            
        # deal turn 
        elif(self.game_phase == 'flop'):
            self.turn = self.deck.draw()
            self.game_phase = 'turn'
            
        # deal river
        elif(self.game_phase == 'turn'):
            self.river = self.deck.draw()
            self.game_phase = 'river'
        else:
            print('Error dealing cards, unexpected game phase of: ' + self.game_phase)

    # get all the cards a certain player has not seen
    def get_undrawn_cards(self, player_num):
        hand = self.players[player_num].hand
        public = self.flop.copy()

        if(self.turn != None):
            public.append(self.turn)
        if(self.river != None):
            public.append(self.river)

        total_seen = hand + public

        deck = Deck(shuffle=False).deck

    def get_public_card_list(self):
        public_card_list = []
        
        if(self.flop != []):
            public_card_list += self.flop
        if(self.turn != None):
            public_card_list.append(self.turn)
        if(self.river != None):
            public_card_list.append(self.river)

        return public_card_list
            
    # check if all but 1 players have folded
    def have_all_but_one_folded(self):
        non_folded_counter = 0 # number of players still in game
        
        for player in self.players:
            if(player.folded == False):
                non_folded_counter += 1

        if(non_folded_counter == 0):
            print("Error: all players have folded")
            exit(0)
        elif(non_folded_counter == 1):
            return True
        else:
            return False
            
    # calculate the winner of the game. Find the rank and highcard of each players hand. The player with the highest rank wins. If two players tie in rank, player with the high card wins. If the high card ties, the game is a tie
    def calculate_winner(self):
        winning_player_rank      = None
        winning_player_high_card = None
        winning_players = []
        
        public_cards = self.flop + [self.turn] + [self.river]

        for player_num in range(0, len(self.players)):
            player = self.players[player_num]
            
            if(player.folded):
                pass

            rank, highcard = self.get_hand_rank(list(player.hand), public_cards)
            # no other players have been considered
            if(winning_player_rank == None):
                winning_player_rank      = rank
                winning_player_high_card = highcard
                winning_players          = [player_num]
            # current player has a better rank than the previous highest
            elif(rank > winning_player_rank):
                winning_player_rank      = rank
                winning_player_high_card = highcard
                winning_players          = [player_num]
            # current player has the same rank as the previous highest
            elif(rank == winning_player_rank):
                # a flush can possibly have no high card (flush is entirely made up from public cards). These conditions account for it
                # current winner and current player has flush but no high card
                if( (rank == RANK_FLUSH) and (highcard == None) and (winning_player_high_card == None) ):
                    winning_players.append(player_num)
                # current player has a high card and current winner does not
                elif( (rank == RANK_FLUSH) and (highcard != None) and (winning_player_high_card == None) ):
                    winning_player_rank      = rank
                    winning_player_high_card = highcard
                    winning_players          = [player_num]
                # current winner has high card and current player does not
                elif( (rank == RANK_FLUSH) and (highcard == None) and (winning_player_high_card != None) ):
                    pass
                # end of flush conditions
                elif(highcard > winning_player_high_card):
                    winning_player_rank      = rank
                    winning_player_high_card = highcard
                    winning_players          = [player_num]
                    
                # if the player has a matching rank and highcard, consider them for a tie. They need to be considered as another play may also tie, or outrank them and win.
                elif(highcard == winning_player_high_card):
                    winning_players.append(player_num)
                        
        self.set_winner(winning_players)

        if(len(winning_players) > 1):
            self.ended_in_tie = True

    
            
    def set_winner(self, winning_players):
        for player_num in range(0, len(self.players)):
            if(player_num in winning_players):
                self.players[player_num].winner = True
            else:
                self.players[player_num].winner = False
        
    def check(self, player_num):
        self.players[player_num].checked = True

    def uncheck_all(self):
        for player in self.players:
            player.checked = False

    def set_players_remaining(self):
        player_counter = 0

        for player in self.players:
            if(player.folded == False):
                player_counter += 1

        self.players_remaining = player_counter

    # finds the next non-folded player, sets the acting player to that player
    def next_acting_player(self):

        # search all player numbers from the current player up
        for i in range(self.acting_player, self.num_players):
            player = self.players[i]
            if(player.number == self.acting_player):
                pass
            elif(player.folded == False):
                return player.number

        # loop around to player 0->current player if not already found
        for i in range(0, self.acting_player):
            player = self.players[i]
            if(player.number == self.acting_player):
                pass
            elif(player.folded == False):
                return player.number

        print("Could not increment acting player, no unfolded player other than the current acting player found!")
        exit(0)        
        
    # calculate valid bets.
    # args: for_children: determines if this is being called to calculate the valid children of a node. If it is, it will ignore the cash stack of the player, and return all bets legal by the rules of limit poker
    def calculate_valid_bets(self, for_children=False):
        valid_bets = [FOLD]
        current_player = self.players[self.acting_player]

        # player has already matched current contribution, and can thus check
        if(current_player.bet == self.contribution):
            valid_bets.append(CHECK)

        contribution_diff = self.contribution - current_player.bet
            
        # player can match current contribution
        if( (for_children == True) or
            ((contribution_diff > 0) and (current_player.cash > contribution_diff))):
            valid_bets.append(contribution_diff)

        # player raises
        if(self.bet_counter < 4):
            if( (for_children == True) or (current_player.cash > (contribution_diff + BIG_BLIND) ) ):
                valid_bets.append(contribution_diff + BIG_BLIND)

        return valid_bets
            
    # bet size is -1 for fold, 0 for check, and either 2 or 4
    # first, calculate to total players contribution to the pot for the game.
    # then, see if this contribution is equal to the current contribution
    # if greater, see if the increase (raise amount) is valid (i.e. 1 big blind), and that no more than 4 bets have been made this round. If it is, increment the bet counter
    # 
    def place_bet(self, bet_size):
        current_player = self.players[self.acting_player]
        
        # player folds
        if(bet_size == FOLD):
            current_player.folded = True
            if(self.have_all_but_one_folded()):
                self.game_complete = True
                winning_player = self.next_acting_player()
                self.players[winning_player].winner = True
                return
            
        #player checks
        elif(bet_size == CHECK):
            if(current_player.bet != self.contribution):
                print("Player attempted to check when player has not met the current contribution")
                exit(0)
            current_player.checked = True
            
        # player matches bet
        elif((current_player.bet + bet_size) == self.contribution):
            current_player.checked = True
            current_player.cash -= bet_size
            current_player.bet  += bet_size
            self.pot            += bet_size
            
        # player raises
        elif( (current_player.bet + bet_size) > self.contribution ):
            if(self.bet_counter > 4):
                print("Attempted to bet when 4 bets have already been made")
                exit(0)
                
            raise_amount = (current_player.bet + bet_size) - self.contribution
            if(raise_amount != BIG_BLIND):
                print("Bet attempt was too high, attempted to raise ", raise_amount)
                exit(0)

            current_player.bet  += bet_size
            current_player.cash -= bet_size
            self.contribution   += raise_amount
            self.pot            += bet_size
            self.bet_counter    += 1
            self.uncheck_all()
            current_player.checked = True
            
        else:
            print("Bet attempted it was illegal, something went wrong")
            print("player num: ", current_player)
            print("bet_size: ", bet_size)
            print("game phase: ", self.game_phase)
            exit(0)

        self.acting_player = self.next_acting_player()
        
        if( self.all_have_checked() == True ):
            self.goto_next_game_phase()

    def end_the_game(self):
        self.game_complete = True
        self.calculate_winner()
        
                
    def goto_next_game_phase(self):
        #print("Betting for " + self.game_phase + " has ended. Moving to next round...")
        
        if(self.game_phase == 'river'):
            self.end_the_game()
        else:
            self.bet_counter = 0
            self.uncheck_all()
            self.deal_community()       
    
    # returns true if all remaining players have checked
    def all_have_checked(self):
        for player in self.players:
            if( (player.checked == False) and (player.folded == False) ):
                return False
        return True

    # this is a hack to keep memory usage under 500gb, so the AI will fold on crappy hands instead of making useless nodes that would be folded on anyways (e.g. low rank, no pair)
    def player_has_crappy_hand(self, player_num):
        hand = self.players[player_num].hand

        # flush potential isn't crappy
        if(hand[0].suit == hand[1].suit):
            return False
        # pocket pair isn't crappy
        if(hand[0].rank == hand[1].rank):
            return False

        # low no pair/flush is crappy
        if(hand[0].rank < 9 and hand[1].rank < 9):
            return True

        # everything else isn't crappy
        return False
    
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
            return RANK_STRAIGHT_FLUSH, high_card_rank

        four_of_a_kind, high_card_rank = self.is_four_of_a_kind(sorted_cards[:])
        if(four_of_a_kind):
            return RANK_FOUR_OF_A_KIND, high_card_rank

        full_house, high_card_rank = self.is_full_house(sorted_cards[:])
        if(full_house):
            return RANK_FULL_HOUSE, high_card_rank

        flush, high_card_rank = self.is_flush(hand[:], public_cards[:])
        if(flush):
            return RANK_FLUSH, high_card_rank

        straight, high_card_rank = self.is_straight(sorted_cards[:])
        if(straight):
            return RANK_STRAIGHT, high_card_rank

        three_of_a_kind, high_card_rank = self.is_three_of_a_kind(sorted_cards[:])
        if(three_of_a_kind):
            return RANK_THREE_OF_A_KIND, high_card_rank

        two_pair, high_card_rank = self.is_two_pair(sorted_cards[:])
        if(two_pair):
            return RANK_TWO_PAIR, high_card_rank

        pair, high_card_rank = self.is_pair(sorted_cards[:])
        if(pair):
            return RANK_PAIR, high_card_rank

        return RANK_HIGH_CARD, self.get_high_card(hand[:])


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
