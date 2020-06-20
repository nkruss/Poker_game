import random
from player_class import *
from hand_class import *
from cards_deck import *
from calc_winner import *

player_1 = Player(1,500)
player_2 = Player(2,500)
player_3 = Player(3,500)

players = [player_1, player_2, player_3]

table = Hand()
deck = Deck()

for i in range(7):
    for player in players:
        card = deck.draw_card()
        player.hand.add_up_card(card)

player_4 = Player(4,500)
players.append(player_4)

card_1 = Card("8", "Hearts", 0)
card_2 = Card("2", "Hearts", 0)
card_3 = Card("2", "Clubs", 0)
card_4 = Card("4", "Hearts", 0)
card_5 = Card("Queen", "Hearts", 0)
card_6 = Card("8", "Clubs", 0)
card_7 = Card("10", "Clubs", 0)

player_4.hand.add_up_card(card_1)
player_4.hand.add_up_card(card_2)
player_4.hand.add_up_card(card_3)
player_4.hand.add_up_card(card_4)
player_4.hand.add_up_card(card_5)
player_4.hand.add_up_card(card_6)
player_4.hand.add_up_card(card_7)


string = ""
for player in players:
    player.reveal_hand(True)
    player.best_hand = determine_hand_high(player, table.cards, ["Queen", "7"])
    print(player.best_hand)
