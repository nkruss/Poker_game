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
# players = []
deck = Deck()

for i in range(7):
    for player in players:
        card = deck.draw_card()
        player.hand.add_up_card(card)

# player_4 = Player(4,500)
# players.append(player_4)
#
# card_1 = Card("7", "Hearts", 0)
# card_2 = Card("8", "Clubs", 0)
# card_3 = Card("3", "Hearts", 0)
# card_4 = Card("Jack", "Hearts", 0)
# card_5 = Card("Ace", "Hearts", 0)
# card_6 = Card("8", "Clubs", 0)
# card_7 = Card("10", "Clubs", 0)
#
# player_4.hand.add_up_card(card_1)
# player_4.hand.add_up_card(card_2)
# player_4.hand.add_up_card(card_3)
# player_4.hand.add_up_card(card_4)
# player_4.hand.add_up_card(card_5)
# player_4.hand.add_up_card(card_6)
# player_4.hand.add_up_card(card_7)
#
player_5 = Player(5,500)
players.append(player_5)

card_1 = Card("3", "Hearts", 0)
card_2 = Card("3", "Hearts", 0)
card_3 = Card("3", "Clubs", 0)
card_4 = Card("Ace", "Hearts", 0)
card_5 = Card("2", "Hearts", 0)
card_6 = Card("5", "Clubs", 0)
card_7 = Card("7", "Clubs", 0)

player_5.hand.add_up_card(card_1)
player_5.hand.add_up_card(card_2)
player_5.hand.add_up_card(card_3)
player_5.hand.add_up_card(card_4)
player_5.hand.add_up_card(card_5)
player_5.hand.add_up_card(card_6)
player_5.hand.add_up_card(card_7)


string = ""
for player in players:
    player.reveal_hand(True)
    determine_hand_high(player, table.cards, ["3", "9"])
    determine_hand_low(player, table.cards, ["3", "9"])
    print("High-", player.high_hand[0])
    print("Low-", player.low_hand[0])
    print()

high_winners = calculate_high_winner(players)
print()
print("High winners -", high_winners)

low_winners = calculate_low_winner(players)
print()
print("Low winners -", low_winners)
