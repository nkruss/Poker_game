from cards_deck import *

class Hand():
    def __init__(self):
        self.cards = []

    def __str__(self):
        if len(self.cards) == 0:
            return "empty"

        string = ascii_version_of_hand(self.cards)
        return string

    def add_up_card(self, card: "Card"):
        self.cards.append(card)

    def add_down_card(self, card: "Card"):
        card.type = "down"
        self.cards.append(card)

    def remove_card(self, card: "Card"):
        self.cards.remove(card)

    def reset(self):
        self.cards = []

    def size(self):
        return len(self.cards)

    def show_hand(self):
        for card in self.cards:
            print(card)
        print()

    def reoreder_hand(self, order_list):
        """
        order_list is a list of the indexes of the cards to order
        """

        ordered = []
        for index in order_list:
            ordered.append(self.cards[index])
        self.cards = ordered

    def elevator_display(self):
        string = "Table: "
        string += "\n" + ascii_version_of_hand(self.cards[:4])
        if self.cards[4].type == "down":
            string += "\n" + ascii_version_of_hidden_card(self.cards[4])
        else:
            string += "\n" + ascii_version_of_card(self.cards[4])
        string += "\n" + ascii_version_of_hand(self.cards[5:])
        return string

    def coded_str_hand(self, player, deck_code):
        if len(self.cards) == 0:
            return "empty"

        string = ascii_version_of_hand(self.cards, current_player=player, deck_code=deck_code)
        return string
