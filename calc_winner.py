import random
from player_class import *
from hand_class import *
from cards_deck import *

def calculate_high_winner(player_list, players_going_high):
    """
    Function to determine the high winner out of the players declaired for going
    high.

    Returns list of winning players
    """
    winners = []
    for player in player_list:
        if player.name in players_going_high:
            #if no current winner set current player to winner
            if len(winners) == 0:
                winners = [player]
            #if player has better hand then current winner set winner to current player
            elif player.high_hand[1] > winners[0].high_hand[1]:
                winners = [player]
            #if player has a hand as good as current player add them to the winner list
            elif player.high_hand[1] == winners[0].high_hand[1]:
                winners.append(player)

    return winners

def calculate_low_winner(player_list, players_going_low):
    """
    Function to determine the low winner out of the players declaired for going
    low.

    Returns list of winning players
    """
    winners = []
    for player in player_list:
        if player.name in players_going_low:
            if len(winners) == 0:
                winners = [player]
            elif player.low_hand[1] > winners[0].low_hand[1]:
                winners = [player]
            elif player.low_hand[1] == winners[0].low_hand[1]:
                winners.append(player)

    return winners

def calculate_down_spade_winner(player_list):
    """
    Function to determine which player has the highest down spade (Ace's are high)

    Returns list containing the winning player
    """
    ranks = ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
    winners = []
    high_spade_rank = 100
    for player in player_list:
        for card in player.hand.cards:
            if card.suit == "Spades" and card.type == "down":
                if len(winners) == 0:
                    winners.append(player)
                    high_spade_rank = ranks.index(card.rank)
                elif ranks.index(card.rank) < high_spade_rank:
                    winners = [player]
                    high_spade_rank = ranks.index(card.rank)
    return winners

def determine_hand_high(player, table_cards, wild_cards: list):
    """
    Calculate the strength of a players high hand and store the hand strength
    in the players score property

    Wild_cards is a list of the ranks of the possible wild cards for the current
    game.

    When calculating hand each type of hand is given a score based off of it's
    place within the hand hierachy (score = hand_index * 1000). Then to
    differentiat between the strength of hands of the same hand type, ranks are
    subtracted from the score
    """

    ranks = ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7", "6", "5", "4", "3", "2", "Ace"]
    hand_order = ["high_card", "pair", "2_pair", "3_of_kind", "straight", "flush", "full_house", "4_of_kind", "straight_flush", "5_of_kind"]

    hand_ranks = {}
    hand_suits = {}
    remaining_ranks_in_hand = []
    num_wilds = 0
    high_hand = None

    #process player hands
    possible_cards = player.hand.cards + table_cards
    for card in possible_cards:
        #determine number of wild cards in player hand
        if card.rank in wild_cards:
            num_wilds += 1
        else:
            #determine number of each rank type that is in player hand
            if card.rank not in hand_ranks:
                hand_ranks[card.rank] = 1
                remaining_ranks_in_hand.append(ranks.index(card.rank))
            else:
                hand_ranks[card.rank] += 1

            #determine card suit infomation about cards in player hand
            if card.suit not in hand_suits:
                hand_suits[card.suit] = [card.rank]
            else:
                hand_suits[card.suit].append(card.rank)

    #determine best set hand
    ## set = (num_cards in set, set_rank)
    highest_set = (0, "2")
    second_highest_set = (0, "2")
    for key in hand_ranks:

        #found new highest set
        if hand_ranks[key] > highest_set[0]:
            second_highest_set = highest_set
            highest_set = (hand_ranks[key], key)
        #found a set using the same number of cards
        elif hand_ranks[key] == highest_set[0]:
            #if new set's rank is higher value shift the previous set to second
            #position and update highest set
            if ranks.index(key) < ranks.index(highest_set[1]):
                second_highest_set = highest_set
                highest_set = (hand_ranks[key], key)
            elif hand_ranks[key] > second_highest_set[0] or ranks.index(key) <= ranks.index(second_highest_set[1]):
                second_highest_set = (hand_ranks[key], key)
        #found a new second best set
        elif hand_ranks[key] > second_highest_set[0]:
            second_highest_set = (hand_ranks[key], key)
        #Equal number but better card
        elif hand_ranks[key] == second_highest_set[0]:
            if ranks.index(key) <= ranks.index(second_highest_set[1]):
                second_highest_set = (hand_ranks[key], key)

    #property for determining the best found hand
    current_best = 0

    #5 of kind
    if highest_set[0] >= 5 - num_wilds:
        high_hand = f"5 of a Kind - {highest_set[1]}'s"
        current_best = hand_order.index("5_of_kind")
        score = (current_best * 1000) - (ranks.index(highest_set[1]) * 10)
    #4 of kind
    elif highest_set[0] == 4 - num_wilds:
        high_hand = f"4 of a Kind - {highest_set[1]}'s"
        current_best = hand_order.index("4_of_kind")
        remaining_ranks_in_hand.remove(ranks.index(highest_set[1]))
        remaining_ranks_in_hand.sort()
        score = (current_best * 1000) - (ranks.index(highest_set[1]) * 10) - remaining_ranks_in_hand[0]
    #full house
    elif highest_set[0] == 3 - num_wilds and second_highest_set[0] >= 2:
        high_hand = f"Full House - {highest_set[1]}'s over {second_highest_set[1]}'s"
        current_best = hand_order.index("full_house")
        score = (current_best * 1000) - (ranks.index(highest_set[1]) * 10) - (ranks.index(second_highest_set[1]))
    #3 of kind
    elif highest_set[0] == 3 - num_wilds:
        high_hand = f"3 of a Kind - {highest_set[1]}'s"
        current_best = hand_order.index("3_of_kind")
        remaining_ranks_in_hand.remove(ranks.index(highest_set[1]))
        remaining_ranks_in_hand.sort()
        score = (current_best * 1000) - (ranks.index(highest_set[1]) * 100)
        for i in range(2):
            score -= remaining_ranks_in_hand[i]
    #2 pair
    elif highest_set[0] == 2 and second_highest_set[0] == 2:
        high_hand = f"2 Pair - {highest_set[1]}'s and {second_highest_set[1]}'s"
        current_best = hand_order.index("2_pair")
        remaining_ranks_in_hand.remove(ranks.index(highest_set[1]))
        remaining_ranks_in_hand.remove(ranks.index(second_highest_set[1]))
        remaining_ranks_in_hand.sort()
        score = (current_best * 1000) - (ranks.index(highest_set[1]) * 10) - (ranks.index(second_highest_set[1]))
        for i in range(1):
            score -= remaining_ranks_in_hand[i]
    #pair
    elif highest_set[0] == 2 - num_wilds:
        high_hand = f"Pair - {highest_set[1]}'s"
        current_best = hand_order.index("pair")
        remaining_ranks_in_hand.remove(ranks.index(highest_set[1]))
        remaining_ranks_in_hand.sort()
        score = (current_best * 1000) - (ranks.index(highest_set[1]) * 10)
        for i in range(3):
            score -= remaining_ranks_in_hand[i]
    else:
        high_hand = f"{highest_set[1]} High"
        current_best = hand_order.index("high_card")
        remaining_ranks_in_hand.sort()
        score = (current_best * 1000)
        for i in range(5):
            score -= remaining_ranks_in_hand[i]

    #check flush
    flush_exists = False
    for key in hand_suits:
        if len(hand_suits[key]) >= 5 - num_wilds:
            flush_exists = True

            rank_index_list = []

            #get ranks of cards that a person has in their hand
            for rank in hand_suits[key]:
                rank_index_list.append(ranks.index(rank))

            #add ranks of wild cards
            for i in range(num_wilds):
                for rank_i in range(len(ranks)):
                    if rank_i not in rank_index_list:
                        rank_index_list.append(rank_i)
                        break

            #get score of the flush
            rank_index_list.sort()
            flush_score = (hand_order.index("flush") * 1000)
            for i in range(len(rank_index_list)):
                flush_score -= (rank_index_list[i] * (2 ** i))

            #check if this flush is better then another flush player has
            if score < flush_score:
                high_hand = f"Flush - {ranks[rank_index_list[0]]} high"
                current_best = hand_order.index("flush")
                score = flush_score

    #check for straight flush
    if flush_exists and current_best != hand_order.index("5_of_kind"):
        best_straight_flush_i = 14
        for suit in hand_suits:
            if len(hand_suits[suit]) >= 5 - num_wilds:
                straight_flush_exists = False
                for start_rank_i in range(len(ranks)):
                    straight_count = 0
                    if ranks[start_rank_i] in hand_suits[suit]:
                        straight_count += 1
                        for offset in range(1,5):
                            if start_rank_i + offset > 13:
                                pass
                            elif (ranks[start_rank_i + offset] in hand_suits[suit]):
                                straight_count += 1
                            if straight_count >= 5 - num_wilds and best_straight_flush_i > max(0, start_rank_i - 4 + offset):
                                high_hand = f"Straight Flush - {ranks[max(0, start_rank_i - 4 + offset)]} high"
                                best_straight_flush_i = max(0, start_rank_i - 4 + offset)
                                current_best = hand_order.index("straight_flush")
                                score = (current_best * 1000) - max(0, start_rank_i - 4 + offset)
                                straight_flush_exists = True
                                break
                        if straight_flush_exists == True:
                            break

    #check straight
    if current_best < hand_order.index("straight"):
        straight_exists = False
        for start_rank_i in range(len(ranks)):
            straight_count = 0
            if ranks[start_rank_i] in hand_ranks:
                straight_count += 1
                for offset in range(1,5):
                    if start_rank_i + offset > 13:
                        pass
                    elif (ranks[start_rank_i + offset] in hand_ranks):
                        straight_count += 1
                    if straight_count >= 5 - num_wilds:
                        high_hand = f"Straight - {ranks[max(0, start_rank_i - 4 + offset)]} high"
                        current_best = hand_order.index("straight")
                        score = (current_best * 1000) - max(0, start_rank_i - 4 + offset)
                        straight_exists = True
                        break
                if straight_exists == True:
                    break

    if player.high_hand[1] <= score:
        player.high_hand = (high_hand, score)
        #print(f"{high_hand} - {possible_cards[0]}, {possible_cards[1]}, {possible_cards[2]}, {possible_cards[3]}, {possible_cards[4]}")

def determine_hand_low(player, table_cards, wild_cards: list):
    """
    wild_cards is a list of the ranks of the possible wild cards
    """

    ranks = ["King", "Queen", "Jack", "10", "9", "8", "7", "6", "5", "4", "3", "2", "Ace"]

    hand_ranks = {}
    remaining_ranks_in_hand = []
    num_wilds = 0
    low_hand = None

    #process player hands
    possible_cards = player.hand.cards + table_cards
    for card in possible_cards:
        if card.rank in wild_cards:
            num_wilds += 1
        else:
            if card.rank not in hand_ranks:
                hand_ranks[card.rank] = 1
                remaining_ranks_in_hand.append(ranks.index(card.rank))
            else:
                hand_ranks[card.rank] += 1

    if len(hand_ranks) + num_wilds >= 5:
        remaining_ranks_in_hand.sort()
        used_wilds = []

        low_hand = ""
        low_hand_i = []

        score = 0
        for i in range(5 - num_wilds,0,-1):
            low_hand_i.append(remaining_ranks_in_hand[-i])
        for i in range(num_wilds):
            for j in range(12):
                if (12 - j) not in low_hand_i:
                    low_hand_i.append(12-j)
                    used_wilds.append(12-j)
                    break

        low_hand_i.sort()
        count = 4
        for i in low_hand_i:
            low_hand = low_hand + ',' + ranks[i]
            score += i * (10 ** count)
            count -= 1

        low_hand = low_hand[1:]
    else:
        score = 0

    if player.low_hand[1] <= score:
        player.low_hand = (low_hand, score)

def determine_winner_0_54(player_list, players_going_high, players_going_low):
    """
    Create 2 lists of players. One for the players who won high, the other for
    the players who won low.

    Return a tuple that contains both created lists
    """

    low_winners = []
    high_winners = []
    for player in player_list:
        #check to see if given player is going low
        if player.name in players_going_low:
            #get player score
            player.low_score = 0
            for card in player.hand.cards:
                if card.rank == "Ace":
                    player.low_score += 1
                elif len(card.rank) > 1:
                    player.low_score += 10
                else:
                    player.low_score += int(card.rank)
            if len(low_winners) == 0:
                low_winners.append(player)
            elif player.low_score < low_winners[0].low_score:
                low_winners = [player]
            elif player.low_score == low_winners[0].low_score:
                low_winners.append(player)

            #print(f"{player.name}: low score = {player.low_score}")

        #check to see if given player is going high
        if player.name in players_going_high:
            #get player score
            player.high_score = 0
            for card in player.hand.cards:
                if card.rank == "Ace":
                    player.high_score += 11
                elif len(card.rank) > 1:
                    player.high_score += 10
                else:
                    player.high_score += int(card.rank)
            if len(high_winners) == 0:
                high_winners.append(player)
            elif player.high_score > high_winners[0].high_score:
                high_winners = [player]
            elif player.high_score == high_winners[0].high_score:
                high_winners.append(player)

            #print(f"{player.name}: high score = {player.high_score}")

    return (high_winners, low_winners)

def determine_winner_7_27(player_list, players_going_high, players_going_low):
    """
    Create 2 lists of players. One for the players who won high, the other for
    the players who won low.

    Return a tuple that contains both created lists
    """

    low_winners = []
    high_winners = []
    for player in player_list:
        #check to see if given player is going low
        if player.name in players_going_low:
            #get player score
            player.low_score = 0
            for card in player.hand.cards:
                if card.rank == "Ace":
                    player.low_score += 1
                elif card.rank == "10":
                    player.low_score += 10
                elif len(card.rank) > 1:
                    player.low_score += .5
                else:
                    player.low_score += int(card.rank)
            #determine if they have a better or equal score to the current winner
            if len(low_winners) == 0 and player.low_score <= 7:
                low_winners.append(player)
            elif player.low_score < low_winners[0].low_score:
                low_winners = [player]
            elif player.low_score == low_winners[0].low_score:
                low_winners.append(player)

            #print(f"{player.name}: low score = {player.low_score}")

        #check to see if given player is going high
        if player.name in players_going_high:
            num_Aces = 0
            #get player score
            player.high_score = 0
            for card in player.hand.cards:
                if card.rank == "Ace":
                    player.high_score += 11
                    num_Aces += 1
                elif card.rank == "10":
                    player.high_score += 10
                elif len(card.rank) > 1:
                    player.high_score += .5
                else:
                    player.high_score += int(card.rank)

            #using aces insure hand score is less then or equal to 27
            for i in range(num_Aces):
                if player.high_score > 27:
                    player.high_score -= 10

            #determine if they have a better or equal score to the current winner
            if len(high_winners) == 0 and player.high_score <= 27:
                high_winners.append(player)
            elif player.high_score > high_winners[0].high_score and player.high_score <= 27:
                high_winners = [player]
            elif player.high_score == high_winners[0].high_score:
                high_winners.append(player)

            #print(f"{player.name}: high score = {player.high_score}")

    return (high_winners, low_winners)

def determine_elivator_hands(player, table, wild_cards: list):

    table_hands = []
    #get all different valid 3 card combos from the table
    for i in range(4):
        cards = [table.cards[i], table.cards[4], table.cards[5+i]]
        table_hands.append(cards)

        card_i = []
        for j in range(i+1,4):
            card_i.append(j)
        for k in range(0, i):
            card_i.append(k)

        table_hands.append([table.cards[card_i[0]], table.cards[card_i[1]], table.cards[card_i[2]]])
        table_hands.append([table.cards[card_i[0] + 5], table.cards[card_i[1] + 5], table.cards[card_i[2] + 5]])

    entire_player_hand = player.hand

    for i in range(4):
        for j in range(i+1, 4):
            #get two cards from player hand
            blank_hand = Hand()
            blank_hand.add_up_card(entire_player_hand.cards[i])
            blank_hand.add_up_card(entire_player_hand.cards[j])
            player.hand = blank_hand
            #look at each 3 card table combo with chosen two cards
            for table_op in table_hands:
                determine_hand_high(player, table_op, wild_cards)
                determine_hand_low(player, table_op, wild_cards)

    player.hand = entire_player_hand
    # print(player.name)
    # print("high hand: ", player.high_hand)
    # print("low hand: ", player.low_hand)

    return None

def determine_king_hands(player, table, direction):
    table_hand = []

    if direction == "row":
        table_hand = [table.cards[1], table.cards[2], table.cards[3]]
    elif direction == "col":
        table_hand = [table.cards[0], table.cards[2], table.cards[4]]
    elif direction == "double":
        table_hand = [table.cards[0], table.cards[1]]
    else:
        table_hand = [table.cards[2], table.cards[3], table.cards[4]]

    determine_hand_high(player, table_hand, [])

    return None

def determine_omaha_hands(player, table, wild_cards: list):
    """
    Function for determining the best had a player has in a omaha game using
    two cards from the table. Looks at every possible combination of cards in
    player hand and cards on the table to determine the best hand.
    """
    table_hands = []

    #set up different combinations of cards from the table
    table_hands.append([table.cards[0], table.cards[1], table.cards[2]])
    table_hands.append([table.cards[0], table.cards[1], table.cards[3]])
    table_hands.append([table.cards[0], table.cards[1], table.cards[4]])
    table_hands.append([table.cards[0], table.cards[2], table.cards[3]])
    table_hands.append([table.cards[0], table.cards[2], table.cards[4]])
    table_hands.append([table.cards[0], table.cards[3], table.cards[4]])
    table_hands.append([table.cards[1], table.cards[2], table.cards[3]])
    table_hands.append([table.cards[1], table.cards[2], table.cards[4]])
    table_hands.append([table.cards[1], table.cards[3], table.cards[4]])
    table_hands.append([table.cards[2], table.cards[3], table.cards[4]])

    entire_player_hand = player.hand

    for i in range(4):
        for j in range(i+1, 4):
            #get two cards from player hand
            blank_hand = Hand()
            blank_hand.add_up_card(entire_player_hand.cards[i])
            blank_hand.add_up_card(entire_player_hand.cards[j])
            player.hand = blank_hand
            #look at each 3 card table combo with chosen two cards
            for table_op in table_hands:
                determine_hand_high(player, table_op, wild_cards)
                determine_hand_low(player, table_op, wild_cards)

    player.hand = entire_player_hand

    return None
