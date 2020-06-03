import random
from player_class import *
from hand_class import *
from cards_deck import *

class Game():
    #finish working on 1 card pass the trash

    def __init__(self, gametype: str, players: list, dealer_i: int, auntie: int):
        #need to implement 7 card screw?, 0-54, elivator?, kings?

        self.pot = 0
        self.dealer_i = dealer_i

        self.players = players[dealer_i:] + players[:dealer_i]

        cheap_games = ["Nicks"]
        norm_games = ["Baseball", "Queens", "Whores", "Texas", "Omaha", "0/54", "7_card_screw", "Elevator", "D_and_G"]

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

        #will use for holdem elivator and kings
        self.table_hand = []

        if gametype == "Baseball":
            #still need to figure out buying fours
            self.rules = "7 card stud: 3's and 9's wild. 4 can buy an extra card"
            self.dealtype = "baseball"
        elif gametype == "Queens":
            self.rules = "7 card stud: queens are wild and card following latest up queen is wild"
            self.dealtype = "sevencard"
        elif gametype == "Whores":
            self.rules = "7 card stud: queens are wild and card following latest up queen is wild, high hand splits with high spade"
            self.dealtype = "sevencard_split"
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
            self.rules = "Kings: ___"
            self.dealtype = "kings"

    def __str__(self):
        if self.dealtype == "elevator":
            if self.game_over:
                string = f"\n\n{self.gametype}: {self.rules} \nPot is {self.pot}\n"
                string += self.table.elevator_display()
            else:
                string = f"\n\n{self.gametype}: {self.rules} \nPot is {self.pot}\n"
                for player in self.players:
                    string += f"{player.name}: chip stack is {player.chip_stack}\n"
                string += self.table.elevator_display()
        elif self.dealtype == "kings":
            string = f"\n\n{self.gametype}: {self.rules} \nPot is {self.pot}\n"
            for player in self.players:
                string += f"{player.name}: chip stack is {player.chip_stack}\n"
            string += self.table.kings_display()
        else:
            string = f"\n\n{self.gametype}: {self.rules} \nPot is {self.pot}\nTable:\n{self.table}\n"
            for player in self.players:
                # string += str(player)
                string += player.coded_str_player(self.deck.deck_code)


        #print to file for dealer
        poker_hands = open('poker_hands.txt', 'w')
        poker_hands.close()
        for player in self.players:
            player.print_hand_to_file()

        return string

    def play(self):

        if self.dealtype == "sevencard":
            self.sevencard()
            self.reveal_all_hands()
            self.winner()

        elif self.dealtype == "sevencard_split":
            #deal type
            self.sevencard()
            #show everyones hand so they can determine who won
            self.reveal_all_hands()
            #pot type
            self.winner_split()

        elif self.dealtype == "holdem":
            self.holdem()
            self.reveal_all_hands()
            self.winner()

        elif self.dealtype == "holdem_split":
            self.omaha()
            print("people declare low or high")
            input("click enter once people have determined if they're going low or high")
            self.reveal_all_hands()
            self.winner_split()

        elif self.dealtype == "nicks":
            self.nicks()

        elif self.dealtype == "0/54":
            self.zero_fifty()
            print("people declare low or high")
            input("click enter once people have determined if they're going low or high")
            self.reveal_all_hands()
            self.winner_split()

        elif self.dealtype == "7_card_screw":
            self.seven_card_screw()
            self.winner_split()

        elif self.dealtype == "elevator":
            self.elevator()
            self.reveal_all_hands()
            self.winner_split()

        elif self.dealtype == "baseball":
            self.baseball()
            self.reveal_all_hands()
            self.winner()

        elif self.dealtype == "1_card_screw":
            self.one_card_screw()

        elif self.dealtype == "D_and_G":
            self.d_and_g()
            self.reveal_all_hands()
            self.winner_split()

        elif self.dealtype == "kings":
            self.kings()

    #game deal functions
    def sevencard(self):
        "game play for 7 card stud"
        while(self.game_over == False):
            #deal two down cards to each player
            self.deal_down(display=False)
            self.deal_down()

            for i in range(4):
                #deal next up card
                self.deal_up()

                #betting for the round
                self.current_bet = 0
                self.betting(self.players)
                if self.game_over == True:
                    break

            if self.game_over == True:
                break

            #final down card
            self.deal_down()

            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            self.game_over = True

    def baseball(self):
        "game play for baseball"
        while(self.game_over == False):
            four_price = 5
            #deal two down cards to each player
            self.deal_down(display=False)
            self.deal_down()
            four_price = self.buy_down_four(four_price)

            for i in range(4):

                #deal next up card
                self.deal_up()
                four_price = self.buy_up_four(four_price)

                #betting for the round
                self.current_bet = 0
                self.betting(self.players)
                if self.game_over == True:
                    break

            if self.game_over == True:
                break

            self.deal_down()
            four_price = self.buy_down_four(four_price)

            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            self.game_over = True

    def holdem(self):
        "game play for holdem deal"
        while(self.game_over == False):
            #deal two down cards to each player
            self.deal_down(display=False)
            self.deal_down()

            #betting pre flop
            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            #flop
            for i in range(3):
                card = self.deck.draw_card()
                self.table.add_up_card(card)
            print(self)

            #betting pre turn
            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            #draw turn
            card = self.deck.draw_card()
            self.table.add_up_card(card)
            print(self)

            #betting pre river
            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            #draw river
            card = self.deck.draw_card()
            self.table.add_up_card(card)
            print(self)

            #betting post river
            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            self.game_over = True

    def omaha(self):
        "game play for holdem deal"
        while(self.game_over == False):
            #deal two down cards to each player
            for i in range(3):
                self.deal_down(display=False)
            self.deal_down()

            #betting pre flop
            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            #flop
            for i in range(3):
                card = self.deck.draw_card()
                self.table.add_up_card(card)
            print(self)

            #betting pre turn
            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            #draw turn
            card = self.deck.draw_card()
            self.table.add_up_card(card)
            print(self)

            #betting pre river
            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            #draw river
            card = self.deck.draw_card()
            self.table.add_up_card(card)
            print(self)

            #betting post river
            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            self.game_over = True

    def nicks(self):
        "game play for nicks deal"

        #get pot cap amount
        self.nick_cap = float(input("Enter pot cap amount:  "))

        #create a new player list to store nick order
        players_original = self.players.copy()
        highest_num_legs = 0

        while(highest_num_legs < 3):
            new_round = True
            while(1==1):
                #add new aunties
                for player in self.players:
                    player.hand.reset()
                    player.auntie(5)
                    self.pot += 5

                someones_in = False
                player_in_index = 0
                player_in_name = ""
                challenged = False

                #if new round
                if new_round:
                    self.deal_down(display=False)
                    self.deal_down()

                else:
                    self.deal_down()

                #loop through players asking who wants to go in
                for player_i in range(len(self.players)):
                    player = self.players[player_i]
                    player_in = input(f"{player.name} are you in y/n? (You have {player.legs} legs)  ")
                    if player_in == "y":
                        someones_in = True
                        player_in_index = player_i
                        player_in_name = player.name
                        player_in = self.players[player_in_index]
                        break

                #loop through player lists again if someone went in
                if someones_in == True:
                    player_list = self.players[player_in_index+1:] + self.players[:player_in_index]
                    challenger_list = []
                    #side bets
                    for player in player_list:
                        player_challenging = input(f"{player.name} are you in challenging {player_in_name} y/n? (they have {player.legs} legs)  ")
                        if player_challenging == "y":
                            challenger_list.append(player)
                            challenged = True

                    #loop through challengers
                    for challenger in challenger_list:
                            print()
                            print(f"{challenger.name}'s cards for {player_in.name} to view")
                            string = "\t"
                            for card in challenger.hand.cards:
                                string += card.encode(player_in, self.deck.deck_code)
                                string += "  "
                            print(string)

                            print(f"{player_in.name}'s cards for {challenger.name} to view")
                            string = "\t"
                            for card in player_in.hand.cards:
                                string += card.encode(challenger, self.deck.deck_code)
                                string += "  "
                            print(string)

                            winner = input(f"who won {challenger.name} or {player_in_name}?  ")
                            self.side_bet(challenger, self.players[player_in_index], winner)

                    #hand out leg if no challenge
                    if challenged == False:
                        self.players[player_in_index].legs += 1

                        #break out to start a new round
                        break

                if self.players[0].hand.size() == 5:
                    break

                new_round = False

            #check for an increase in legs
            for player in self.players:
                if highest_num_legs < player.legs:
                    highest_num_legs = player.legs

            #rotate dealer
            self.dealer_i += 1
            #loop the dealer
            if self.dealer_i > len(self.players)-1:
                self.dealer_i = 0
            self.players = players_original[self.dealer_i:] + players_original[:self.dealer_i]

            #reset Deck
            self.deck = Deck()

        #give pot to the winner
        for player in self.players:
            if player.legs == 3:
                player.chip_stack += self.pot
            player.legs = 0

    def zero_fifty(self):
        "game play for 0/54 deal"
        while(self.game_over == False):
            #deal 5 down cards to each player
            for i in range(4):
                self.deal_down(display=False)
            self.deal_down()

            #fliping up cards
            for i in range(5):
                #bet pre card flip
                self.current_bet = 0
                self.betting(self.players)
                if self.game_over == True:
                    break

                flipped_card_new = False
                while(flipped_card_new == False):

                    flipped_card_new = True
                    #flip an up card
                    flipped_card = self.deck.draw_card()
                    for card in self.table.cards:
                        if card.rank == flipped_card.rank:
                            flipped_card_new = False

                    self.table.add_up_card(flipped_card)

                for player in self.players:
                    for card in player.hand.cards:
                        if card.rank == flipped_card.rank:
                            player.hand.cards.remove(card)
                print(self)

            #last round of betting
            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            self.game_over = True

    def seven_card_screw(self):
        "game play for 7 card screw your neigbor deal"
        up_or_down = input("Are we passing down or up D/U?  ")
        while(self.game_over == False):
            #deal 7 down cards to all players
            for i in range(6):
                self.deal_down(display=False)
            self.deal_down()

            #pass 3
            self.passing_cards(up_or_down, 3)
            #pass 2
            self.passing_cards(up_or_down, 2)
            #pass 1
            self.passing_cards(up_or_down, 1)

            #discard 2
            self.discarding_cards(2)

            #reorder hands
            self.players_reorder_hands(5)
            print(self)


            for i in range(5):
                self.current_bet = 0
                self.betting(self.players)
                if self.game_over == True:
                    break

                for player in self.players:
                    player.reveal_card(i)

                if i != 4:
                    print(self)

            print("people declare low or high")
            input("click enter once people have determined if they're going low or high")
            print(self)

            self.game_over = True

    def elevator(self):
        "game play for elevator deal"
        while(self.game_over == False):

            #deal cards to table
            for i in range(9):
                card = self.deck.draw_card()
                self.table.add_down_card(card)

            #deal four down cards to each player
            for i in range(3):
                self.deal_down(display=False)
            self.deal_down()

            #print player hands
            string = ''
            for player in self.players:
                string += player.coded_str_player(self.deck.deck_code)
            print(string)

            #betting pre card flip
            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            #list to store down card positions
            down_list = [0,1,2,3,5,6,7,8]
            for i in range(4):

                card1_index = random.choice(down_list)
                down_list.remove(card1_index)
                card2_index = random.choice(down_list)
                down_list.remove(card2_index)

                self.table.cards[card1_index].type = "up"
                self.table.cards[card2_index].type = "up"

                print(self)

                #betting pre card flip
                self.current_bet = 0
                self.betting(self.players)
                if self.game_over == True:
                    break

            #flip middle card
            self.table.cards[4].type = "up"
            print(self)

            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            print("people declare low or high")
            input("click enter once people have determined if their going low or high")
            self.game_over = True

    def one_card_screw(self):
        "game play for one card pass the trash"

        players_original = self.players.copy()

        #create a dictonary of the players where the player's name is the key
        #and the key value is whether or not the player is still in
        player_dic = {}
        for player in self.players:
            player_dic[player.name] = True

        up_or_down = input("Are we passing down or up D/U?  ")
        stack_num = input("How many stacks of 5 chips are each person going to start with?  ")
        self.pot = (int(stack_num) * 5) * len(self.players)
        for player in self.players:
            player.chip_stack -= (int(stack_num) * 5)
            player.legs = int(stack_num)

        while(len(self.players) != 1):

            #reset deck if not enough cards
            if len(self.deck.cards) < len(self.players) + 1:
                print("New Deck")
                self.deck = Deck()

            #deal everyone 1 card
            self.deal_down()

            #loop through players asking who wants to go in
            for player_i in range(len(self.players)):
                player = self.players[player_i]
                player_in = input(f"{player.name} are you passing y/n? (You have {player.legs} stacks left)  ")
                #case for last person
                if player_in == "y" and (player ==  self.players[-1]):
                    player.hand.cards[0] = self.deck.draw_card()
                elif player_in == "y":
                    next_player = self.players[player_i + 1]
                    player_card = player.pass_cards([0])
                    next_player_card = next_player.pass_cards([0])
                    player_card = player_card[0]
                    next_player_card = next_player_card[0]

                    player.hand.add_down_card(next_player_card)
                    next_player.hand.add_down_card(player_card)

                    print(self)

            #show everyones hands
            self.reveal_all_hands()

            #remove legs from loosers
            losser_recorded = False
            while(losser_recorded == False):
                try:
                    losser = input("Who had the lowest card? (Enter player name), if no losser enter 'none'   ")
                    for player in self.players:
                        if player.name == losser:
                            player.legs -= 1
                            losser_i = self.players.index(player)
                            losser_recorded = True
                    if losser == "none":
                        losser_recorded = True
                except:
                    print("error processing losser try again")

            player_eliminated = False
            #check if anyone is out of legs
            for player in self.players:
                if player.legs == 0:
                    player_dic[player.name] = False
                    player_eliminated = True


            #loop the dealer
            if self.dealer_i >= len(players_original) - 1:
                self.dealer_i = 0

            elif player_eliminated == True:
                pass

            else:
                #rotate dealer
                self.dealer_i += 1

            self.players = []
            for player_i in range(self.dealer_i, len(players_original)):
                player_name = players_original[player_i].name
                #check if player is still in game and if so add them to the player list
                if player_dic[player_name] == True:
                    self.players.append(players_original[player_i])

            for player_i in range(self.dealer_i):
                player_name = players_original[player_i].name
                #check if player is still in game and if so add them to the player list
                if player_dic[player_name] == True:
                    self.players.append(players_original[player_i])

            #reset players hands
            for player in self.players:
                player.hand.reset()

        #give pot to the winner
        self.players[0].chip_stack += self.pot

    def d_and_g(self):
        "game play for David and Goliath"
        up_value = float(input("How much do you want to charge for the last card to come up?  "))
        while(self.game_over == False):
            #deal two down cards to each player
            self.deal_down(display=False)
            self.deal_down()

            for i in range(4):
                #deal next up card
                self.deal_up()

                #betting for the round
                self.current_bet = 0
                self.betting(self.players)
                if self.game_over == True:
                    break

            if self.game_over == True:
                break

            #final down card
            for player in self.players:
                card_type = input(f"{player.name} do you want your last card up for {up_value} (y/n)?   ")
                if card_type == "y":
                    card = self.deck.draw_card()
                    player.hand.add_up_card(card)
                    player.chip_stack -= up_value
                    self.pot += up_value
                else:
                    card = self.deck.draw_card()
                    player.hand.add_down_card(card)
            print(self)


            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            self.game_over = True

    def kings(self):
        "game play for kings deal"

        #get pot cap amount
        kings_cap = float(input("Enter pot cap amount:  "))

        #create a new player list to store nick order
        players_original = self.players.copy()

        #have people put in initial antie amounts
        for player in self.players:
            player.auntie(5)
            self.pot += 5

        while(self.game_over == False):

            #deal cards to table
            for i in range(9):
                card = self.deck.draw_card()
                self.table.add_down_card(card)

            self.table.cards[0].type = "up"
            self.table.cards[1].type = "up"

            #deal four down cards to each player
            for i in range(2):
                self.deal_down(display=False)
            self.deal_down()

            #print player hands
            string = ''
            for player in self.players:
                string += player.coded_str_player(self.deck.deck_code)
            print(string)

            #loop through players asking who wants to go in
            players_in = []
            for player_i in range(len(self.players)):
                player = self.players[player_i]
                player_in = input(f"{player.name} are you in y/n?  ")
                if player_in == "y":
                    while(1==1):
                        position = input(f" {player.name} are you in blind, row, col, or double?  ")
                        if position in ["blind", "row", "col", "double"]:
                            break
                        else:
                            print("Error processing where you wanted to go in")
                    players_in.append((player, position))

            #display table with all cards flipped
            for card in self.table.cards:
                card.type = "up"
            print(self)
            self.reveal_all_hands()

            #get payout amount
            if self.pot > kings_cap:
                payout = kings_cap
            else:
                payout = self.pot

            num_losers = 0
            for player_tuple in players_in:
                print(f"{player_tuple[0].name} you went in the {player_tuple[1]}")
                result = input(f" {player_tuple[0].name} did you win, lose, or tie (w/l/t)?  ")

                #double or nothing condition
                if result == "w":
                    player_tuple[0].chip_stack +=  payout
                    self.pot -= payout
                elif result == "l" and player_tuple[1] == "double":
                    player_tuple[0].chip_stack -=  (2 * payout)
                    self.pot += (2 * payout)
                    num_losers += 1
                elif result == "t":
                    num_losers += 1
                else:
                    player_tuple[0].chip_stack -= payout
                    self.pot += payout
                    num_losers += 1

            #end game condition
            if num_losers == 0 and len(players_in) == 1:
                player_tuple[0].chip_stack +=  self.pot
                self.game_over = True

            #reset players hands, deck, and table hand, rotate deal
            else:
                self.deck = Deck()
                self.table.cards = []
                for player in self.players:
                    player.hand.reset()

                #rotate dealer
                self.dealer_i += 1
                #loop the dealer
                if self.dealer_i > len(self.players)-1:
                    self.dealer_i = 0
                self.players = players_original[self.dealer_i:] + players_original[:self.dealer_i]


    #helpfull functions
    def passing_cards(self, pass_direction, num_cards):
        """Function for passing [num_cards] in each players hand in the
        [pass_direction]"""

        for player in self.players:
            pass_recorded = False
            while(pass_recorded == False):
                cards_to_pass = input(f"{player.name} what {num_cards} cards to you want to pass (cards are ordered 1-7 left to right) (input indexes as A,B,...)?  ")
                try:
                    cards_to_pass = cards_to_pass.split(',')

                    #check to make sure corrent number of cards was inputed if
                    ##not create error to get to except statement
                    if len(cards_to_pass) != num_cards:
                         raise Exception()

                    #shift to zero indexed
                    for index_i in range(len(cards_to_pass)):
                        cards_to_pass[index_i] = int(cards_to_pass[index_i]) - 1

                    cards_to_pass = player.pass_cards(cards_to_pass)
                    pass_recorded = True
                except:
                    print("error passing try again")

            if pass_direction == "U":
                #find player being passed to
                current_player_index = self.players.index(player)
                #loop around players if at the end of the list
                if current_player_index == 0:
                    next_player = self.players[len(self.players)-1]
                else:
                    next_player = self.players[current_player_index - 1]

                #add passed cards to next persons hand
                for card in cards_to_pass:
                    next_player.hand.add_up_card(card)

            elif pass_direction == "D":
                #find player being passed to
                current_player_index = self.players.index(player)
                #loop around players if at the end of the list
                if current_player_index == len(self.players) - 1:
                    next_player = self.players[0]
                else:
                    next_player = self.players[current_player_index + 1]

                #add passed cards to next persons hand
                for card in cards_to_pass:
                    next_player.hand.add_up_card(card)
        print(self)

    def discarding_cards(self, num_cards):
        for player in self.players:
            discard_recorded = False
            while(discard_recorded == False):
                cards_to_discard = input(f"{player.name} what {num_cards} cards to you want to discard (cards are ordered 1-7 left to right) (input indexes as A,B,...)?  ")
                try:
                    cards_to_discard = cards_to_discard.split(',')

                    #check to make sure corrent number of cards was inputed if
                    ##not create error to get to except statement
                    if len(cards_to_discard) != num_cards:
                        raise Exception()

                    #shift to zero indexed
                    for index_i in range(len(cards_to_discard)):
                        cards_to_discard[index_i] = int(cards_to_discard[index_i]) - 1

                    counter = 0
                    for card_i in cards_to_discard:
                        cards_to_discard[counter] = player.hand.cards[card_i]
                        counter += 1

                    discard_recorded = True
                except:
                    print("error passing try again")

            for card in cards_to_discard:
                player.hand.remove_card(card)

        print(self)

    def buy_down_four(self, four_price):
        "returns new four_price"
        for player in self.players:
            four_recorded = False
            while(four_recorded == False):
                try:
                    four_bought = input(f"{player.name} are you buying a down four for {four_price} y/n?  ")

                    if four_bought == 'y':

                        four_found = False

                        #flip down four
                        for card in player.hand.cards:
                            if card.type == "down" and card.rank == "4":
                                card.type = "up"

                                #pay for four
                                player.chip_stack -= four_price
                                #increase four_price
                                four_price += 5

                                #give new down card
                                card = self.deck.draw_card()
                                card.type = "down"
                                player.hand.cards.append(card)

                                print(self)

                                break

                        if four_found == False:
                            print("Error processing buying of four. System shows you do not have a four.")


                    else:
                        four_recorded = True

                except:
                    print("error processing buying of four, try again")
        return four_price

    def buy_up_four(self, four_price):
        "returns new four_price"
        for player in self.players:
            if player.hand.cards[-1].rank == '4':
                four_recorded = False
                while(four_recorded == False):
                    try:
                        four_bought = input(f"{player.name} are you buying a up four for {four_price} y/n?  ")

                        if four_bought == 'y':
                            #pay for four
                            player.chip_stack -= four_price
                            #increase four_price
                            four_price += 5
                            #flip down four
                            player.hand.cards[-1].type = "up"
                            #give new down card
                            card = self.deck.draw_card()
                            card.type = "up"
                            player.hand.cards.append(card)

                            print(self)

                            if player.hand.cards[-1].rank == "4":
                                pass
                            else:
                                four_recorded = True

                        else:
                            four_recorded = True

                    except:
                        print("error processing buying of four, try again")
        return four_price

    def players_reorder_hands(self, num_cards):
        for player in self.players:
            reorder_recorded = False
            while(reorder_recorded == False):
                try:
                    order_list = input(f"{player.name} what order do you want your hand A,B,C...?  ")

                    order_list = order_list.split(',')

                    #check to make sure corrent number of cards was inputed if
                    ##not create error to get to except statement
                    if len(order_list) != num_cards:
                         raise Exception()

                    #shift to zero indexed
                    for index_i in range(len(order_list)):
                        order_list[index_i] = int(order_list[index_i]) - 1

                    player.hand.reoreder_hand(order_list)

                    reorder_recorded = True
                except:
                    print("error processing ordering try again")

    def side_bet(self, player1: "Player", player2: "Player", winner: str):
        #check if pot is larger then the cap
        if self.pot > self.nick_cap:
            payout = self.nick_cap
        else:
            payout = self.pot

        if player1.name == winner:
            player1.chip_stack += payout
            player2.chip_stack -= payout
        else:
            player1.chip_stack -= payout
            player2.chip_stack += payout

    def reveal_all_hands(self):
        string = ""
        if self.winning_player != None:
            return None
        else:
            for player in self.players:
                player.reveal_hand()

    def all_fold(self):
        everyone_folded = False

        if len(self.players) == 1:
            everyone_folded = True
            self.winning_player = self.players[0]

        self.game_over = everyone_folded

    def winner(self):
        if self.winning_player != None:
            self.winning_player.chip_stack += self.pot
            return None

        winner_recorded = False
        while(winner_recorded == False):
            try:
                winners = input("Who is the winner? (Enter player name [if tie seperate names by ','])   ")

                winning_players = winners.split(",")
                payout = self.pot / len(winning_players)

                for player in self.players:
                    if player.name in winning_players:
                        player.chip_stack += payout
                        winner_recorded = True
            except:
                print("error processing winner try again")

    def winner_split(self):
        if self.winning_player != None:
            self.winning_player.chip_stack += self.pot
            return None

        winner_recorded = False
        while(winner_recorded == False):
            try:
                print("special input ")
                winners = input("Who is the winner? (Enter winners names in the form high_winners:low_winners)  ")
                #for only one person winning enter them as "player_name:"
                high_low = winners.split(":")
                high_winners = high_low[0].split(",")
                low_winners = high_low[1].split(",")

                #possible winner senerios
                if high_winners[0] == '':
                    low_winnings = self.pot / len(low_winners)
                elif low_winners[0] == '':
                    high_winnings = self.pot / len(high_winners)
                else:
                    low_winnings = (self.pot / 2) / len(low_winners)
                    high_winnings = (self.pot / 2) / len(high_winners)


                #possible winner senerios
                if len(high_winners) == 0:
                    low_winnings = self.pot
                elif len(low_winners) == 0:
                    high_winnings = self.pot

                #confirm whether inputed names awards out the proper amount of money
                awarded_chips = 0
                for player in self.players:
                    if player.name in low_winners:
                        awarded_chips += low_winnings
                    elif player.name in high_winners:
                        awarded_chips += high_winnings

                if awarded_chips != self.pot:
                    #throw error
                    error = []
                    print(error[2])

                #award people their winnings
                for player in self.players:
                    if player.name in low_winners:
                        player.chip_stack += low_winnings
                    elif player.name in high_winners:
                        player.chip_stack += high_winnings


                winner_recorded = True

            except:
                print("error processing winner try again")

    def deal_up(self):
        for player in self.players:
            card = self.deck.draw_card()
            player.hand.add_up_card(card)
        print(self)

    def deal_down(self, display=True):
        for player in self.players:
            card = self.deck.draw_card()
            player.hand.add_down_card(card)
        if display:
            print(self)

    def betting(self, player_list):
        #get bet for every player
        was_raise = False
        current_players = player_list.copy()
        for player in current_players:

            #if players already matched the bet pass
            if (player.bet == self.current_bet) and (player.bet != 0):
                pass

            #get player to call bet
            else:
                player.bet += self.bet(player, self.current_bet)

                #check if there was a raise
                if (player.bet > self.current_bet):
                    was_raise = True

                #update current bet minimum
                if player.bet > self.current_bet:
                    self.current_bet = player.bet

        #if there was a raise add another round of betting
        if was_raise == True:
            self.betting(self.players)

        #reset player bets
        for player in self.players:
            player.bet = 0

        #check if everyone folded
        self.all_fold()

    def bet(self, player, current_bet: int):
        bet_recorded = False
        while(bet_recorded == False):
            try:
                bet_action = input(f"{player.name} what is action (fold, check, call, raise)? current bet is {current_bet} you have {player.bet} in:  ")

                #deal with fold
                if bet_action == "fold":
                    self.players.remove(player)
                    return 0

                #deal with check
                if bet_action == "check":
                    #if bets not equal to zero create error to get new bet imput
                    if current_bet != 0:
                        raise Exception("Can't check. Current bet is not zero")
                    else:
                        bet = 0

                #deal with call
                if bet_action == "call":
                    bet = current_bet - player.bet

                if bet_action == "raise":
                    bet = input(f"what is your raise?:  ")
                    bet = current_bet - player.bet + float(bet)

                bet = float(bet)
                #exchange money
                player.chip_stack -= bet
                self.pot += bet

                bet_recorded = True
            except:
                print("error processing bet try again")

        return bet
