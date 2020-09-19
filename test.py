import random
from player_class import *
from hand_class import *
from cards_deck import *
from calc_winner import *

player_1 = Player("N",500)
player_2 = Player("T",500)
player_3 = Player("M",500)

players = [player_1, player_2, player_3]

table = Hand()
players = []
deck = Deck()

# for i in range(2):
#     for player in players:
#         card = deck.draw_card()
#         player.hand.add_down_card(card)
# for i in range(4):
#     for player in players:
#         card = deck.draw_card()
#         player.hand.add_up_card(card)
# for i in range(1):
#     for player in players:
#         card = deck.draw_card()
#         player.hand.add_down_card(card)

# for i in range(9):
#     card = deck.draw_card()
#     table.add_down_card(card)

player_4 = Player(4,500)
players.append(player_4)

card_1 = Card("Ace", "Hearts", 0)
card_2 = Card("7", "Hearts", 0)
card_3 = Card("4", "Hearts", 0)
card_4 = Card("Jack", "Hearts", 0)
card_5 = Card("10", "Hearts", 0)
card_6 = Card("3", "Clubs", 0)
card_7 = Card("2", "Clubs", 0)

player_4.hand.add_up_card(card_1)
player_4.hand.add_up_card(card_2)
player_4.hand.add_up_card(card_3)
player_4.hand.add_up_card(card_4)
player_4.hand.add_up_card(card_5)
player_4.hand.add_up_card(card_6)
player_4.hand.add_up_card(card_7)

player_5 = Player(5,500)
players.append(player_5)

card_1 = Card("Ace", "Hearts", 0)
card_2 = Card("6", "Hearts", 0)
card_3 = Card("5", "Hearts", 0)
card_4 = Card("Jack", "Hearts", 0)
card_5 = Card("10", "Hearts", 0)
card_6 = Card("3", "Clubs", 0)
card_7 = Card("2", "Clubs", 0)

player_5.hand.add_up_card(card_1)
player_5.hand.add_up_card(card_2)
player_5.hand.add_up_card(card_3)
player_5.hand.add_up_card(card_4)
player_5.hand.add_up_card(card_5)
player_5.hand.add_up_card(card_6)
player_5.hand.add_up_card(card_7)


# print("down spade")
# # string = ""
# winner = calculate_down_spade_winner(players)
# for player in players:
#     player.reveal_hand(True)
# if len(winner) == 0:
#     print("no down spade")
# else:
#     print(winner[-1].name, "won")

#standard hand check
string = ""
for player in players:
    player.reveal_hand(True)
    determine_hand_high(player, table.cards, [])
    determine_hand_low(player, table.cards, [])
    print("High-", player.high_hand[0])
    print("Low-", player.low_hand[0])
    print()

high_winners = calculate_high_winner(players, [4,5])
print("High winners -")
for player in high_winners:
    print(player.name)


low_winners = calculate_low_winner(players, [4,5])
print()
print("Low winners -", low_winners)


#
# print("\n7/27 score")
# high_winners, low_winners = determine_winner_7_27(players, ["N","T","M"], ["N","T","M"])
# print("High winners:")
# for player in high_winners:
#     print(player.name)
# print("Low winners:")
# for player in low_winners:
#     print(player.name)


# #Elevator test
# for card in table.cards:
#     card.type = "up"
# print(table.elevator_display(True))
# for player in players:
#     player.reveal_hand(True)
#     determine_elivator_hands(player, table, [table.cards[4].rank])
#
# high_winners = calculate_high_winner(players, ["N","T","M"])
# print()
# for player in high_winners:
#     print("High winners -", player.name, player.high_hand)
# low_winners = calculate_low_winner(players, ["N","T","M"])
# print()
# for player in low_winners:
#     print("Low winners -", player.name, player.low_hand)
