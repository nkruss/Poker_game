import random

#code to add different colors to cards
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BLACK = '\x1b[30m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def ascii_version_of_card(*cards, return_string=True, current_player=None, deck_code=None):
    #got off internet
    """
    Instead of a boring text version of the card we render an ASCII image of the card.
    :param cards: One or more card objects
    :param return_string: By default we return the string version of the card, but the dealer hide the 1st card and we
    keep it as a list so that the dealer can add a hidden card in front of the list
    """
    # we will use this to prints the appropriate icons for each card
    suits_name = ['Spades', 'Diamonds', 'Hearts', 'Clubs', ' ']
    suits_actual_symbols = ['♠', '♦', '♥', '♣', ' ']
    suits_symbols = ['S', 'D', 'H', 'C', ' ']

    # create an empty list of list, each sublist is a line
    lines = [[] for i in range(9)]

    for index, card in enumerate(cards):
        # "King" should be "K" and "10" should still be "10"
        if card.rank == '10':  # ten is the only one who's rank is 2 char long
            rank = card.rank
            space = ''  # if we write "10" on the card that line will be 1 char to long
        else:
            rank = card.rank[0]  # some have a rank of 'King' this changes that to a simple 'K' ("King" doesn't fit)
            space = ' '  # no "10", we use a blank space to will the void
        # get the cards suit in two steps
        suit_i = suits_name.index(card.suit)
        suit = suits_symbols[suit_i]
        suit_sym = suits_actual_symbols[suit_i]

        # print(color.BOLD + 'Hello World !' + color.END)

        if current_player != None:
            if suit == 'H' or suit == 'D':
                card = cards[0]
                # add the individual card on a line by line basis
                lines[0].append('┌─────────┐')
                lines[1].append('│{}{}      {}│'.format(color.RED + rank + color.END, space, color.RED + suit_sym + color.END))  # use two {} one for char, one for space or char
                lines[2].append('│         │')
                lines[3].append('│         │')
                lines[4].append('│    {}    │'.format(color.RED + suit + color.END))
                lines[5].append(f"│  ({card.encode(current_player, deck_code)})  │")
                lines[6].append('│         │')
                lines[7].append('│{}      {}{}│'.format(color.RED + suit_sym + color.END, space, color.RED + rank + color.END))
                lines[8].append('└─────────┘')

            else:
                card = cards[0]
                # add the individual card on a line by line basis
                lines[0].append('┌─────────┐')
                lines[1].append('│{}{}      {}│'.format(color.CYAN + rank + color.END, space, color.CYAN + suit_sym + color.END))  # use two {} one for char, one for space or char
                lines[2].append('│         │')
                lines[3].append('│         │')
                lines[4].append('│    {}    │'.format(color.CYAN + suit + color.END))
                lines[5].append(f"│  ({card.encode(current_player, deck_code)})  │")
                lines[6].append('│         │')
                lines[7].append('│{}      {}{}│'.format(color.CYAN + suit_sym + color.END, space, color.CYAN + rank + color.END))
                lines[8].append('└─────────┘')

        else:
            # add the individual card on a line by line basis
            if suit == 'H' or suit == 'D':
                lines[0].append('┌─────────┐')
                lines[1].append('│{}{}      {}│'.format(color.RED + rank + color.END, space, color.RED + suit_sym + color.END))
                lines[2].append('│         │')
                lines[3].append('│         │')
                lines[4].append('│    {}    │'.format(color.RED + suit + color.END))
                lines[5].append('│         │')
                lines[6].append('│         │')
                lines[7].append('│{}      {}{}│'.format(color.RED + suit_sym + color.END, space, color.RED + rank + color.END))
                lines[8].append('└─────────┘')

            else:
                lines[0].append('┌─────────┐')
                lines[1].append('│{}{}      {}│'.format(color.CYAN + rank + color.END, space, color.CYAN + suit_sym + color.END))
                lines[2].append('│         │')
                lines[3].append('│         │')
                lines[4].append('│    {}    │'.format(color.CYAN + suit + color.END))
                lines[5].append('│         │')
                lines[6].append('│         │')
                lines[7].append('│{}      {}{}│'.format(color.CYAN + suit_sym + color.END, space, color.CYAN + rank + color.END))
                lines[8].append('└─────────┘')


    result = []
    for index, line in enumerate(lines):
        result.append(''.join(lines[index]))

    # hidden cards do not use string
    if return_string:
        return '\n'.join(result)
    else:
        return result

def ascii_version_of_hidden_card(*cards, return_string=True, current_player=None, deck_code=None):
    """
    Essentially the dealers method of print ascii cards. This method hides the first card, shows it flipped over
    :param cards: A list of card objects, the first will be hidden
    :return: A string, the nice ascii version of cards
    """
    if current_player != None:
        card = cards[0]
        lines = [['┌─────────┐'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], [f"│░░░{card.encode(current_player, deck_code)}░░░│"], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['└─────────┘']]
    else:
        # a flipper over card. # This is a list of lists instead of a list of string becuase appending to a list is better then adding a string
        lines = [['┌─────────┐'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['└─────────┘']]

    # store the non-flipped over card after the one that is flipped over
    cards_except_first = ascii_version_of_card(*cards[1:], return_string=False)
    for index, line in enumerate(cards_except_first):
        lines[index].append(line)

    # make each line into a single list
    for index, line in enumerate(lines):
        lines[index] = ''.join(line)

    # # convert the list into a single string
    # return '\n'.join(lines)

    # hidden cards do not use string
    if return_string:
        return '\n'.join(lines)
    else:
        return lines

def ascii_version_of_hand(cards, current_player=None, deck_code=None):
    """
    Essentially the dealers method of print ascii cards. This method hides the first card, shows it flipped over
    :param cards: A list of card objects, the first will be hidden
    :return: A string, the nice ascii version of cards
    """
    lines = [[] for i in range(9)]


    for card in cards:
        if card.type == "up":
            current_line = ascii_version_of_card(card, return_string=False, current_player=current_player, deck_code=deck_code)
        else:
            current_line = ascii_version_of_hidden_card(card, return_string=False, current_player=current_player, deck_code=deck_code)

        for index, line in enumerate(current_line):
            lines[index].append(line)

    # make each line into a single list
    for index, line in enumerate(lines):
        lines[index] = ''.join(line)

    # convert the list into a single string
    return '\n'.join(lines)

class Card(): #need to finish encode function

    def __init__(self, rank: str, suit: str, code_value):
         self.rank = rank
         self.suit = suit
         self.type = "up"
         self.code_value = code_value

    def __str__(self):
        string = f"{self.rank}_of_{self.suit}"
        return string

    def encode(self, player, deck_code):
        "player is the player that the card belongs to"
        card_code = self.code_value + (52 * ((deck_code * player.deck_multiplier) % 887))
        card_code = (card_code + player.card_offset) % 46133
        card_code = (card_code * player.card_multiplier) % 46133

        to_base_36 = {0:"0", 1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9",
                    10:"a", 11:"b", 12:"c", 13:"d", 14:"e", 15:"f", 16:"g", 17:"h", 18:"i", 19:"j",
                    20:"k", 21:"L", 22:"m", 23:"n", 24:"o", 25:"p", 26:"q", 27:"r", 28:"s", 29:"t",
                    30:"u", 31:"v", 32:"w", 33:"x", 34:"y", 35:"z"
                    }

        first_char = to_base_36[card_code // (36**2)]
        second_char = to_base_36[(card_code // 36) % 36]
        third_char = to_base_36[card_code % 36]

        code = first_char + second_char + third_char
        return code

class Deck():

    def __init__(self):
        self.cards = []
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        suits = ["Hearts", "Spades", "Clubs", "Diamonds"]
        code_value = 0
        for suit in suits:
            for rank in ranks:
                card = Card(rank, suit, code_value)
                self.cards.append(card)
                code_value += 1

        self.deck_code = random.randint(0,886)

    def draw_card(self):
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card
