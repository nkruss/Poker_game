from hand_class import *
from cards_deck import *

class Player(): #need to finish making encription key

    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.chip_stack = 500
        self.bet = 0
        self.legs = 0

        #create random key
        self.deck_multiplier = random.randint(1, 886)
        self.card_offset = random.randint(0, 46132)
        self.card_multiplier = random.randint(1, 46132)

        player_info = open('player_info.txt', 'a')
        info_string = f"{self.name}\n"
        info_string += f"card offset = {self.card_offset}, card multiplayer = {self.card_multiplier}, deck_multiplier = {self.deck_multiplier}"
        print(info_string, file=player_info)


    def aunti(self, amount):
        self.chip_stack -= amount

    def __str__(self):
        return f"{self.name}: chip stack is {self.chip_stack}, hand is \n{str(self.hand)}\n"

    def reveal_hand(self):
        for card in self.hand.cards:
            card.type = "up"
        print(f"{self.name}\n{self.hand}")

    def reveal_card(self, index):
        self.hand.cards[index].type = "up"

    def pass_cards(self, cards: list):
        """
        cards = list of indexes of cards to pass
        returns a list of the cards passed
        """
        #get cards to pass
        passing_cards = []
        for card_i in cards:
            passing_cards.append(self.hand.cards[card_i])
        #remove passed cards from players hand
        for card in passing_cards:
            self.hand.remove_card(card)
        return passing_cards

    def print_hand_to_file(self):
        poker_hands = open('poker_hands.txt', 'a')
        hand_string = f"{self.name}\n"
        # down_indexes = []
        # for card in self.hand.cards:
        #     if card.type == "down":
        #         card.type = "up"
        #         index = self.hand.cards.index(card)
        #         down_indexes.append(index)
        # hand_string += ascii_version_of_hand(self.hand.cards)
        # print(hand_string, file=poker_hands)
        # poker_hands.close()
        #
        # for index in down_indexes:
        #     self.hand.cards[index].type = "down"

        for card in self.hand.cards:
            hand_string += f"{card}, "
        print(hand_string, file=poker_hands)
        return None

    def coded_str_player(self, deck_code):
        return f"{self.name}: chip stack is {self.chip_stack}, hand is \n{self.hand.coded_str_hand(self, deck_code)}\n"
