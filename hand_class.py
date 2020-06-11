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
        """Add card to hand (card type is up)"""
        self.cards.append(card)

    def add_down_card(self, card: "Card"):
        """Add card to hand (card type is down)"""
        card.type = "down"
        self.cards.append(card)

    def remove_card(self, card: "Card"):
        """Remove target card from hand"""
        self.cards.remove(card)

    def reset(self):
        """Resets hand to being empty"""
        self.cards = []

    def size(self):
        """Return how many cards are in the hand"""
        return len(self.cards)

    def show_hand(self):
        """Function for debuging hand. Print out each card in the hand"""
        for card in self.cards:
            print(card)
        print()

    def display_hand(self, card_color):
        """Function to get string rep of hand without card codes"""
        if len(self.cards) == 0:
            return "empty"

        string = ascii_version_of_hand(self.cards, card_color=card_color)
        return string

    def reoreder_hand(self, order_list):
        """
        order_list is a list of the indexes of the cards to reorder
        """

        ordered = []
        for index in order_list:
            ordered.append(self.cards[index])
        self.cards = ordered

    def elevator_display(self, card_color: bool):
        """Function for gametype elivator. Returns a string display of the table
        state for elivator.
        """

        string = "Table: "
        string += "\n" + ascii_version_of_hand(self.cards[:4], card_color=card_color)
        if self.cards[4].type == "down":
            string += "\n" + ascii_version_of_hidden_card(self.cards[4])
        else:
            string += "\n" + ascii_version_of_card(self.cards[4], card_color=card_color)
        string += "\n" + ascii_version_of_hand(self.cards[5:], card_color=card_color)
        return string

    def kings_display(self, card_color: bool):
        """Function for gametype kings. Returns a string display of the table
        state for kings courners.
        """
        blank_card = Card(" ", " ", 0)

        string = "Table: "

        line_1 = [blank_card, self.cards[0], blank_card]
        line_3 = [blank_card, self.cards[4], blank_card]
        blind = self.cards[5:9]

        string += "\n" + ascii_version_of_hand(line_1, card_color=card_color)
        string += "\n" + ascii_version_of_hand(self.cards[1:4], card_color=card_color)
        string += "\n" + ascii_version_of_hand(line_3, card_color=card_color)

        string += "\n" + "Blind: "
        string += "\n" + ascii_version_of_hand(blind, card_color=card_color) + "\n"

        return string

    def coded_str_hand(self, player, deck_code, card_color):
        if len(self.cards) == 0:
            return "empty"

        string = ascii_version_of_hand(self.cards, current_player=player, deck_code=deck_code, card_color=card_color)
        return string
