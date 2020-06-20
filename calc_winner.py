from game_play import *

def calculate_high_winner(player_list):
    winners = []
    for player in player_list:
        if len(winners) == 0:
            winners = [player]
        elif player.best_hand[1] > winners[0].best_hand[1]:
            winners = [player]
        elif player.best_hand[1] == winners[0].best_hand[1]:
            winners.append(player)

    for winner_i in range(len(winners)):
        winners[winner_i] = winners[winner_i].name

    return winners

def determine_hand_high(player, table_cards, wild_cards: list):
    """
    wild_cards is a list of the ranks of the possible wild cards
    """

    ranks = ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7", "6", "5", "4", "3", "2", "Ace"]
    hand_order = ["high_card", "pair", "2_pair", "3_of_kind", "straight", "flush", "full_house", "4_of_kind", "straight_flush", "5_of_kind"]
    #process player hands
    hand_ranks = {}
    hand_suits = {}
    remaining_ranks_in_hand = []
    num_wilds = 0
    best_hand = None
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

            if card.suit not in hand_suits:
                hand_suits[card.suit] = [card.rank]
            else:
                hand_suits[card.suit].append(card.rank)

    #determine best set hand
    highest_set = (0, "2")
    second_highest_set = (0, "2")
    for key in hand_ranks:

        #found new highest number in a set
        if hand_ranks[key] > highest_set[0]:
            second_highest_set = highest_set
            highest_set = (hand_ranks[key], key)
        #found a set using the same number of cards
        elif hand_ranks[key] == highest_set[0]:
            #if new set's rank is higher shift the previous set to secound
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

        # print("H", highest_set)
        # print("S", second_highest_set)
        # print(key, hand_ranks[key])

    # print(highest_set)
    # print(second_highest_set)

    current_best = 0
    #5 of kind
    if highest_set[0] >= 5 - num_wilds:
        best_hand = f"5 of a Kind - {highest_set[1]}'s"
        current_best = hand_order.index("5_of_kind")
        score = (current_best * 1000) - (ranks.index(highest_set[1]) * 10)
    #4 of kind
    elif highest_set[0] == 4 - num_wilds:
        best_hand = f"4 of a Kind - {highest_set[1]}'s"
        current_best = hand_order.index("4_of_kind")
        remaining_ranks_in_hand.remove(ranks.index(highest_set[1]))
        remaining_ranks_in_hand.sort()
        score = (current_best * 1000) - (ranks.index(highest_set[1]) * 10) - remaining_ranks_in_hand[0]
    #full house
    elif highest_set[0] == 3 - num_wilds and second_highest_set[0] >= 2:
        best_hand = f"Full House - {highest_set[1]}'s over {second_highest_set[1]}'s"
        current_best = hand_order.index("full_house")
        score = (current_best * 1000) - (ranks.index(highest_set[1]) * 10) - (ranks.index(second_highest_set[1]))
    #3 of kind
    elif highest_set[0] == 3 - num_wilds:
        best_hand = f"3 of a Kind - {highest_set[1]}'s"
        current_best = hand_order.index("3_of_kind")
        remaining_ranks_in_hand.remove(ranks.index(highest_set[1]))
        remaining_ranks_in_hand.sort()
        score = (current_best * 1000) - (ranks.index(highest_set[1]) * 100)
        for i in range(2):
            score -= remaining_ranks_in_hand[i]
    #2 pair
    elif highest_set[0] == 2 and second_highest_set[0] == 2:
        best_hand = f"2 Pair - {highest_set[1]}'s and {second_highest_set[1]}'s"
        current_best = hand_order.index("2_pair")
        remaining_ranks_in_hand.remove(ranks.index(highest_set[1]))
        remaining_ranks_in_hand.remove(ranks.index(second_highest_set[1]))
        remaining_ranks_in_hand.sort()
        score = (current_best * 1000) - (ranks.index(highest_set[1]) * 10) - (ranks.index(second_highest_set[1]))
        for i in range(1):
            score -= remaining_ranks_in_hand[i]
    #pair
    elif highest_set[0] == 2 - num_wilds:
        best_hand = f"Pair - {highest_set[1]}'s"
        current_best = hand_order.index("pair")
        remaining_ranks_in_hand.remove(ranks.index(highest_set[1]))
        remaining_ranks_in_hand.sort()
        score = (current_best * 1000) - (ranks.index(highest_set[1]) * 10)
        for i in range(3):
            score -= remaining_ranks_in_hand[i]
    else:
        best_hand = f"{highest_set[1]} High"
        current_best = hand_order.index("high_card")
        remaining_ranks_in_hand.sort()
        score = (current_best * 1000)
        for i in range(5):
            score -= remaining_ranks_in_hand[i]

    #check flush
    flush_exists = False
    for key in hand_suits:
        if (len(hand_suits[key]) >= 5 - num_wilds):
            flush_exists = True

            rank_index_list = []
            for rank in hand_suits[key]:
                rank_index_list.append(ranks.index(rank))
            rank_index_list.sort()
            flush_score = (hand_order.index("flush") * 1000)
            for i in range(5):
                flush_score -= rank_index_list[i]

            if score < flush_score:
                best_hand = f"Flush - {ranks[rank_index_list[0]]} high"
                current_best = hand_order.index("flush")
                score = flush_score

    #check for straight flush
    if flush_exists:
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
                                best_hand = f"Straight Flush - {ranks[max(0, start_rank_i - 4 + offset)]} high"
                                best_straight_flush_i = max(0, start_rank_i - 4 + offset)
                                current_best = hand_order.index("straight_flush")
                                score = (current_best * 1000) - max(0, start_rank_i - 4 + offset)
                                straight_flush_exists = True
                                break
                        if straight_flush_exists == True:
                            break

    #check straight
    # if current_best < hand_order.index("straight")
    #     for start_rank_i in range(len(ranks)-4):
    #         straight_count = 0
    #         for offset in range(5):
    #             if (ranks[start_rank_i + offset] in hand_ranks):
    #                 straight_count += 1
    #         if straight_count >= 5 - num_wilds:
    #             best_hand = f"Straight - {ranks[start_rank_i]} high"
    #             current_best = hand_order.index("straight")
    #             break

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
                        best_hand = f"Straight - {ranks[max(0, start_rank_i - 4 + offset)]} high"
                        current_best = hand_order.index("straight")
                        score = (current_best * 1000) - max(0, start_rank_i - 4 + offset)
                        straight_exists = True
                        break
                if straight_exists == True:
                    break

    return (best_hand, score)

# def determine_hand_high_2_card(player, table, wild_cards: list):
#     """
#     wild_cards is a list of the ranks of the possible wild cards
#     """
#
#     ranks = ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7", "6", "5", "4", "3", "2", "Ace"]
#     hand_order = ["high_card", "pair", "2_pair", "3_of_kind", "straight", "flush", "full_house", "4_of_kind", "staight_flush", "5_of_kind"]
#
#     hand_ranks_table = {}
#     hand_suits_table = {}
#     num_wilds_table = 0
#     for card in table.cards:
#         if card.rank in wild_cards:
#             num_wilds_table += 1
#         else:
#             if card.rank not in hand_ranks_table:
#                 hand_ranks_table[card.rank] = 1
#             else:
#                 hand_ranks_table[card.rank] += 1
#
#             if card.suit not in hand_suits_table:
#                 hand_suits_table[card.suit] = [card.rank]
#             else:
#                 hand_suits_table[card.suit].append(card.rank)
#     num_wilds_table = min(3, num_wilds_table)
#
#     best_hand = None
#
#     for i in range(4):
#         for j in range(i+1, 4):
#             #process player hands
#             hand_ranks = hand_ranks_table
#             hand_suits = hand_suits_table
#             num_wilds = 0
#
#             required_cards = [player.hand.card[i], player.hand.card[j]]
#             for card in required_cards:
#                 if card.rank in wild_cards:
#                     num_wilds += 1
#                 else:
#                     if card.rank not in hand_ranks:
#                         hand_ranks[card.rank] = 1
#                     else:
#                         hand_ranks[card.rank] += 1
#
#                     if card.suit not in hand_suits:
#                         hand_suits[card.suit] = [card.rank]
#                     else:
#                         hand_suits[card.suit].append(card.rank)
#
#             #determine best set using two cards from hand
#             highest_set = (0, None)
#             second_highest_set = (0, None)
#             for key in hand_ranks:
#                 #found new highest number in a set
#                 if hand_ranks[key] > highest_set[0]:
#                     highest_set = (hand_ranks[key], key)
#                 #found a set using the same number of cards
#                 elif hand_ranks[key] == highest_set[0]:
#                     #if new set's rank is higher shift the previous set to secound
#                     #position and update highest set
#                     if ranks.index(key) < highest_set[1]:
#                         second_highest_set = highest_set
#                         highest_set = (hand_ranks[key], key)
#                     else:
#                         second_highest_set = (hand_ranks[key], key)
#                 #found a new second best set
#                 elif hand_ranks[key] > second_highest_set:
#                     second_highest_set = (hand_ranks[key], key)
#                 #Equal number but better card
#                 elif hand_ranks[key] == second_highest_set:
#                     if ranks.index(key) < second_highest_set[1]:
#                         second_highest_set = (hand_ranks[key], key)
#
#             current_best = 0
#             #need to use both
#             if num_wilds == 0:
#                 if ((player.hand.card[i].rank == player.hand.card[j].rank) and
#                     (player.hand.card[i].rank == highest_set[1])):
#
#                     if highest_set[0] >= 5 - (num_wilds + num_wilds_table):
#                         best_hand = f"5 of a Kind - {highest_set[1]}'s"
#                         current_best = hand_order.index("5_of_kind")
#
#
#                 #need to use at least one
#                 elif highest_set[0] == 4 - num_wilds:
#                     best_hand = f"4 of a Kind - {highest_set[1]}'s"
#                     current_best = hand_order.index("4_of_kind")
#                 #need to use both
#                 elif highest_set[0] == 3 - num_wilds and second_highest_set[0] == 2:
#                     best_hand = "Full House - {highest_set[1]}'s over {second_highest_set[1]}'s"
#                     current_best = hand_order.index("full_house")
#                 #need to use none
#                 elif highest_set[0] == 3 - num_wilds:
#                     best_hand = "3 of a Kind - {highest_set[1]}'s"
#                     current_best = hand_order.index("3_of_kind")
#                 #need to use one
#                 elif highest_set[0] == 2 and second_highest_set[0] == 2:
#                     best_hand = "2 Pair - {highest_set[1]}'s and {second_highest_set[1]}'s"
#                     current_best = hand_order.index("2_pair")
#                 #need to use none
#                 elif highest_set[0] == 2 - num_wilds:
#                     best_hand = "Pair - {highest_set[1]}'s"
#                     current_best = hand_order.index("pair")
#                 #need to use none
#                 else:
#                     best_hand = "{highest_set[1]} High"
#                     current_best = hand_order.index("high_card")
#
#             #check flush
#             flush_exists = False
#             for key in hand_suits:
#                 if (len(hand_suits[key]) >= 5 - num_wilds):
#                     flush_exists = True
#                     if current_best < hand_order.index("flush"):
#                         best_hand = "Flush"
#                         current_best = hand_order.index("flush")
#
#             #check for straight flush
#             if flush_exists:
#                 best_straight_flush_i = 14
#                 for suit in hand_suits:
#                     if len(hand_suits[suit]) >= 5 - num_wilds:
#                         straight_flush_exists = False
#                         for start_rank_i in range(len(ranks)-4):
#                             straight_count = 0
#                             if ranks[start_rank_i] in hand_suits[suit]:
#                                 straight_count += 1
#                                 for offset in range(1,5):
#                                     if (ranks[start_rank_i + offset] in hand_suits[suit]):
#                                         straight_count += 1
#                                     if straight_count >= 5 - num_wilds and best_straight_flush_i > max(0, start_rank_i - 4 + offset):
#                                         best_hand = f"Straight Flush - {ranks[max(0, start_rank_i - 4 + offset)]} high"
#                                         best_straight_flush_i = max(0, start_rank_i - 4 + offset)
#                                         current_best = hand_order.index("straight")
#                                         straight_flush_exists = True
#                                         break
#                                 if straight_flush_exists == True:
#                                     break
#
#             #check straight
#             # if current_best < hand_order.index("straight")
#             #     for start_rank_i in range(len(ranks)-4):
#             #         straight_count = 0
#             #         for offset in range(5):
#             #             if (ranks[start_rank_i + offset] in hand_ranks):
#             #                 straight_count += 1
#             #         if straight_count >= 5 - num_wilds:
#             #             best_hand = f"Straight - {ranks[start_rank_i]} high"
#             #             current_best = hand_order.index("straight")
#             #             break
#
#             if current_best < hand_order.index("straight"):
#                 straight_exists = False
#                 for start_rank_i in range(len(ranks)-4):
#                     straight_count = 0
#                     if ranks[start_rank_i] in hand_ranks:
#                         straight_count += 1
#                         for offset in range(1,5):
#                             if (ranks[start_rank_i + offset] in hand_ranks):
#                                 straight_count += 1
#                             if straight_count >= 5 - num_wilds:
#                                 best_hand = f"Straight - {ranks[max(0, start_rank_i - 4 + offset)]} high"
#                                 current_best = hand_order.index("straight")
#                                 straight_exists = True
#                                 break
#                         if straight_exists == True:
#                             break