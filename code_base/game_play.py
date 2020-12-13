from calc_winner import *
from deal_functions import *
from helper_functions import *

class Game(Deals, Game_helper):
    #deal functions can be found in deal_functions.py
    #helper functions can be found in helper_functions.py

    def __init__(self, gametype: str, players: list, dealer_i: int, auntie: int, card_color: bool):

        self.pot = 0
        self.dealer_i = dealer_i
        self.card_color = card_color

        self.players = players[dealer_i:] + players[:dealer_i]

        norm_games = ["Baseball",
                        "Queens",
                        "Whores",
                        "Texas",
                        "Omaha",
                        "0/54",
                        "7_card_screw",
                        "Elevator",
                        "D_and_G",
                        "7/27",
                        "Bipolor"]

        if gametype in norm_games:
            for player in players:
                player.auntie(auntie)
                self.pot += auntie

        self.deck = Deck()
        self.table = Hand()
        self.gametype = gametype
        self.rules = ""
        self.nick_cap = 0
        self.winning_player = None

        self.current_bet = 0
        self.dealtype = None
        self.game_over = False
        self.wilds = []

        if gametype == "Baseball":
            self.rules = "7 card stud: 3's and 9's wild. 4 can buy an extra card"
            self.dealtype = "baseball"
            self.wilds = ["3", "9"]
        elif gametype == "Queens":
            self.rules = "7 card stud: queens are wild and card following latest up queen is wild"
            self.dealtype = "sevencard"
            self.wilds = ["Queen", "Queen"]
        elif gametype == "Whores":
            self.rules = "7 card stud: queens are wild and card following latest up queen is wild, high hand splits with high spade"
            self.dealtype = "sevencard_split"
            self.wilds = ["Queen", "Queen"]
        elif gametype == "Texas":
            self.rules = "Classic holdem"
            self.dealtype = "holdem"
        elif gametype == "Omaha":
            self.rules = "Omaha, holdom with high low split"
            self.dealtype = "holdem_split"
        elif gametype == "Nicks":
            self.rules = "Nicks: 2 card low, 3 card high, 4 card low, 5 card high"
            self.dealtype = "nicks"
        elif gametype == "0/54":
            self.rules = "0/54: 5 cards, if card comes up on the table everyone looses that card from their hand"
            self.dealtype= "0/54"
        elif gametype == "7_card_screw":
            self.rules = "7_card_screw: pass 3, pass 2, pass 1, discard 2, reveals"
            self.dealtype = "7_card_screw"
        elif gametype == "Elevator":
            self.rules = "Elevator: high/low, play 2 cards from hand, middle card of the elevator and all like cards are wild"
            self.dealtype = "elevator"
        elif gametype == "1_card_screw":
            self.rules = "1_card_screw: don't end up with the lowest card (Aces are low)"
            self.dealtype = "1_card_screw"
        elif gametype == "D_and_G":
            self.rules = "David and Goliath: 7 card stud, if you go high lowest down card is wild, if you go low highest down card is wild, last down card can be bought up"
            self.dealtype = "D_and_G"
        elif gametype == "Kings":
            self.rules = "Kings: __"
            self.dealtype = "kings"
        elif gametype == "7/27":
            self.rules = "7/27: Closest to 7 and 27 from below (aces=1 or 11, face-cards=.5), can pass getting aditional card 3 times before hand is locked"
            self.dealtype= "7/27"
        if gametype == "Bipolor":
            self.rules = "7 card stud: Split between queens and baseball. Game shifts to Queen's on up-queen, shifts to Baseball on up 9"
            self.dealtype = "bipolor"

    def __str__(self):
        if self.dealtype == "elevator":
            if self.game_over:
                string = f"\n\n{self.gametype}: {self.rules} \nPot is {self.pot}\n"
                string += self.table.elevator_display(self.card_color)
            else:
                string = f"\n\n{self.gametype}: {self.rules} \nPot is {self.pot}\n"
                for player in self.players:
                    string += f"{player.name}: chip stack is {player.chip_stack}\n"
                string += self.table.elevator_display(self.card_color)
        elif self.dealtype == "kings":
            string = f"\n\n{self.gametype}: {self.rules} \nPot is {self.pot}\n"
            for player in self.players:
                string += f"{player.name}: chip stack is {player.chip_stack}\n"
            string += self.table.kings_display(self.card_color)
        else:
            string = f"\n\n{self.gametype}: {self.rules} \nPot is {self.pot}\nTable:\n{self.table}\n"
            for player in self.players:
                # string += str(player)
                string += player.coded_str_player(self.deck.deck_code, self.card_color)

        return string

    def play(self):

        if self.dealtype == "sevencard":
            self.queens()
            self.winner()
            self.reveal_all_hands()

        elif self.dealtype == "sevencard_split":
            self.queens()
            self.winner()
            self.reveal_all_hands()

        elif self.dealtype == "holdem":
            self.holdem()
            self.winner()
            self.reveal_all_hands()

        elif self.dealtype == "holdem_split":
            self.omaha()
            print("people declare low or high")
            input("click enter once people have determined if they're going low or high")
            self.winner()
            self.reveal_all_hands()

        elif self.dealtype == "nicks":
            self.nicks()

        elif self.dealtype == "0/54":
            self.zero_fifty()
            print("people declare low or high")
            input("click enter once people have determined if they're going low or high")
            self.winner()
            self.reveal_all_hands()

        elif self.dealtype == "7_card_screw":
            self.seven_card_screw()
            self.winner()

        elif self.dealtype == "elevator":
            self.elevator()
            print("people declare low or high")
            input("click enter once people have determined if they're going low or high")
            self.winner()
            self.reveal_all_hands()

        elif self.dealtype == "baseball":
            self.baseball()
            self.winner()
            self.reveal_all_hands()

        elif self.dealtype == "1_card_screw":
            self.one_card_screw()

        elif self.dealtype == "D_and_G":
            self.d_and_g()
            print("people declare low or high")
            input("click enter once people have determined if they're going low or high")
            self.winner()
            self.reveal_all_hands()

        elif self.dealtype == "kings":
            self.kings()

        elif self.dealtype == "7/27":
            self.seven_twentyseven()
            self.winner()
            self.reveal_all_hands()

        elif self.dealtype == "bipolor":
            self.bipolor()
            self.winner()
            self.reveal_all_hands()
