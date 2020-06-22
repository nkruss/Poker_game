from calc_winner import *

class Game():

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
            self.rules = "Kings: ___"
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


        #print to file for dealer
        poker_hands = open('poker_hands.txt', 'w')
        poker_hands.close()
        for player in self.players:
            player.print_hand_to_file()

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

        #need to figure out wild programming
        elif self.dealtype == "D_and_G":
            self.d_and_g()
            print("people declare low or high")
            input("click enter once people have determined if they're going low or high")
            self.winner()
            self.reveal_all_hands()

        #need to figure out adding in blind
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

    #game deal functions
    def queens(self):
        "game play for 7 card stud"
        while(self.game_over == False):
            #deal two down cards to each player
            self.deal_down(display=False)
            self.deal_down(display=False)

            Queen_up = False
            for i in range(4):
                #deal next up card
                self.deal_up()

                #find new wild
                for player in self.players:
                    up_card_rank = player.hand.cards[-1].rank
                    if Queen_up:
                        self.wilds[1] = up_card_rank
                        Queen_up = False
                    if up_card_rank == "Queen":
                        Queen_up = True

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

                if new_round:
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
                    cards_to_remove = []
                    for card in player.hand.cards:
                        if card.rank == flipped_card.rank:
                            cards_to_remove.append(card)
                    for card in cards_to_remove:
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
                string += player.coded_str_player(self.deck.deck_code, self.card_color)
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
            self.wilds = [self.table.cards[4].rank]
            print(self)

            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

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
                    player_eliminated_index = players_original.index(player)


            #loop the dealer
            if self.dealer_i >= len(players_original) - 1:
                self.dealer_i = 0
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

            print("next order:")
            for player in self.players:
                print(player.name)

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

            #deal 3 down cards to each player
            for i in range(2):
                self.deal_down(display=False)
            self.deal_down()

            #print player hands
            string = ''
            for player in self.players:
                string += player.coded_str_player(self.deck.deck_code, self.card_color)
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
            payout = self.pot

            winners = []
            tie = []
            for player_tuple in players_in:
                player = player_tuple[0]
                determine_king_hands(player, self.table, player_tuple[1])

                #if no current winner set current player to winner
                if len(winners) == 0:
                    winners = [player]
                #if player has better hand then current winner set winner to current player
                elif player.high_hand[1] > winners[0].high_hand[1]:
                    winners = [player]
                    tie = []
                #if player has a hand as good as current player add them to the winner list
                elif player.high_hand[1] == winners[0].high_hand[1]:
                    tie.append(winners[0])
                    tie.append(player)

            print()
            print("###############################################################")
            #if only one person is in calculate blinds hand
            if len(players_in) == 1:
                blind = Player("blind", 0)
                blind.hand.cards = self.table.cards[5:]
                determine_king_hands(blind, self.table, "blind")
                #if blind has better hand then current winner set winner to be empty
                if blind.high_hand[1] > winners[0].high_hand[1]:
                    winners = []
                #if tie with blind
                elif blind.high_hand[1] == winners[0].high_hand[1]:
                    tie.append(winners[0])
                    winners = []
                print(f"Blind had {blind.high_hand[0]}")

            #award the money
            num_losers = 0
            for player_tuple in players_in:
                player = player_tuple[0]
                direction = player_tuple[1]
                if player in tie:
                    num_losers += 1
                    print(f"{player.name} you tied with a {player.high_hand[0]}")
                elif player in winners:
                    player.chip_stack += payout
                    self.pot -= payout
                    print(f"{player.name} you won {payout} with a {player.high_hand[0]}")
                elif direction == "double":
                    player.chip_stack -= (2 * min(payout, kings_cap))
                    self.pot += (2 * min(payout, kings_cap))
                    num_losers += 1
                    print(f"{player.name} you lost {(2 * min(payout, kings_cap))} with a {player.high_hand[0]}")
                else:
                    player.chip_stack -= min(payout, kings_cap)
                    self.pot += min(payout, kings_cap)
                    num_losers += 1
                    print(f"{player.name} you lost {min(payout, kings_cap)} with a {player.high_hand[0]}")
            print()
            print("###############################################################")

            #end game condition
            if num_losers == 0 and len(players_in) == 1:
                winners[0].chip_stack += self.pot
                self.game_over = True

            #reset players hands, deck, and table hand, rotate deal
            else:
                self.deck = Deck()
                self.table.cards = []
                for player in self.players:
                    player.reset_hand()

                #rotate dealer
                self.dealer_i += 1
                #loop the dealer
                if self.dealer_i > len(self.players)-1:
                    self.dealer_i = 0
                self.players = players_original[self.dealer_i:] + players_original[:self.dealer_i]

    def seven_twentyseven(self):
        "game play for 7 card stud"
        while(self.game_over == False):
            eligible_players = self.players.copy()

            #deal two down cards to each player
            self.deal_down(display=False)
            self.deal_down()

            for player in self.players:
                player.legs = 0
                up = int(input(f"{player.name} which card do you want flipped (1 or 2)?  "))
                up -= 1
                player.hand.cards[up].type = "up"

            lowest_num_legs = 0

            print(self)

            #betting for the round
            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            #remove player if they folded
            players_to_remove = []
            for player in eligible_players:
                if player not in self.players:
                    players_to_remove.append(player)
            for player in players_to_remove:
                eligible_players.remove(player)

            while(1==1):
                players_to_remove = []

                for player in eligible_players:
                    # if player in eligible_players:
                    hit = input(f"{player.name} (you have {3 - player.legs} passes left) do you want another card y/n?  ")
                    if hit == "y":
                        card = self.deck.draw_card()
                        player.hand.add_up_card(card)
                    else:
                        player.legs += 1

                        #lock players hand
                        if player.legs == 3:
                            players_to_remove.append(player)

                print(self)

                #betting for the round
                self.current_bet = 0
                self.betting(self.players)
                if self.game_over == True:
                    break

                #remove player if they folded
                for player in eligible_players:
                    if player not in self.players and (player not in players_to_remove):
                        players_to_remove.append(player)

                #actual removal of players
                for player in players_to_remove:

                    eligible_players.remove(player)

                #condition to end game
                if len(eligible_players) == 0:
                    print("breaking")
                    break

            self.game_over = True

    def bipolor(self):
        "game play for bipolor"
        while(self.game_over == False):
            baseball = True
            self.wilds = ["3", "9"]

            four_price = 5
            #deal two down cards to each player
            self.deal_down(display=False)
            self.deal_down()
            four_price = self.buy_down_four(four_price)

            Queen_up = False
            for i in range(4):

                #deal next up card
                self.deal_up()

                for player in self.players:
                    if player.hand.cards[-1].rank == "9":
                        baseball = True
                        print("Game changed to Baseball")
                        self.wilds = ["3", "9"]
                    elif player.hand.cards[-1].rank == "Queen":
                        baseball = False
                        print("Game changed to Queens")
                        self.wilds = ["Queen", "Queen"]

                if baseball:
                    four_price = self.buy_up_four(four_price)
                #if Queens find wilds
                else:
                    for player in self.players:
                        up_card_rank = player.hand.cards[-1].rank
                        if Queen_up:
                            self.wilds[1] = up_card_rank
                            Queen_up = False
                        if up_card_rank == "Queen":
                            Queen_up = True

                #betting for the round
                self.current_bet = 0
                self.betting(self.players)
                if self.game_over == True:
                    break

            if self.game_over == True:
                break

            self.deal_down()
            if baseball:
                four_price = self.buy_down_four(four_price)

            self.current_bet = 0
            self.betting(self.players)
            if self.game_over == True:
                break

            self.game_over = True

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
                    print("error discarding try again")

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
                player.reveal_hand(self.card_color)

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

        players_going_high = []
        players_going_low = []

        split_games = ["0/54",
                        "7/27",
                        "7_card_screw",
                        "elevator",
                        "D_and_G",
                        "holdem_split"]

        #get inputs for who is going high and who is going low
        if self.dealtype in split_games:
            player_names = []
            for player in self.players:
                player_names.append(player.name)

            while(1==1):
                try:
                    players = input("Who is going high? Enter names seperated by ' ' (if none click enter).  ")
                    players_going_high = players.split(" ")
                    if players_going_high != []:
                        for name in players_going_high:
                            if name not in player_names:
                                raise Exception()
                    break
                except:
                    print("Error proccessing players going high")

            while(1==1):
                try:
                    players = input("Who is going low? Enter names seperated by ' ' (if none click enter).  ")
                    players_going_low = players.split(" ")
                    if players_going_low != []:
                        for name in players_going_low:
                            if name not in player_names:
                                raise Exception()
                    break
                except:
                    print("Error proccessing players going low")

        # calculate high and low winners
        if self.dealtype == "0/54":

            high_winners, low_winners = determine_winner_0_54(self.players, players_going_high, players_going_low)

        elif self.dealtype == "7/27":

            high_winners, low_winners = determine_winner_7_27(self.player, players_going_high, players_going_low)

        elif self.dealtype == "7_card_screw":

            for player in self.players:
                if player.name in players_going_high:
                    determine_hand_high(player, self.table.cards, self.wilds)
                if player.name in players_going_low:
                    determine_hand_low(player, self.table.cards, self.wilds)

            high_winners = calculate_high_winner(self.players, players_going_high)
            low_winners = calculate_low_winner(self.players, players_going_low)

        elif self.dealtype == "elevator":

            for player in self.players:
                determine_elivator_hands(player, self.table, self.wilds)

            high_winners = calculate_high_winner(self.players, players_going_high)
            low_winners = calculate_low_winner(self.players, players_going_low)

        elif self.dealtype == "sevencard_split":
            for player in self.players:
                determine_hand_high(player, self.table.cards, self.wilds)
                players_going_high.append(player.name)
            high_winners = calculate_high_winner(self.players, players_going_high)

            low_winners = calculate_down_spade_winner(self.players)

        elif self.dealtype == "D_and_G":

            #find down wilds
            ranks = ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
            winners = []
            for player in self.players:
                high_wild = []
                high_wild_rank_index = 0
                low_wild = []
                low_wild_rank_index = 100
                for card in player.hand.cards:
                    if card.type == "down" and card.rank != "Ace":
                        if ranks.index(card.rank) > high_wild_rank_index:
                            high_wild = [card.rank]
                            high_wild_rank_index = ranks.index(card.rank)
                        if ranks.index(card.rank) < low_wild_rank_index:
                            low_wild = [card.rank]
                            low_wild_rank_index = ranks.index(card.rank)

                determine_hand_high(player, self.table.cards, high_wild)
                determine_hand_low(player, self.table.cards, low_wild)

                #print(player.name, high_wild, low_wild)

            high_winners = calculate_high_winner(self.players, players_going_high)
            low_winners = calculate_low_winner(self.players, players_going_low)

        elif self.dealtype == "holdem_split":

            for player in self.players:
                determine_omaha_hands(player, self.table, self.wilds)

            high_winners = calculate_high_winner(self.players, players_going_high)
            low_winners = calculate_low_winner(self.players, players_going_low)

        else:

            for player in self.players:
                determine_hand_high(player, self.table.cards, self.wilds)
                players_going_high.append(player.name)

            high_winners = calculate_high_winner(self.players, players_going_high)
            low_winners = []

        #print best hands for players
        print()
        print("###############################################################")
        for player in self.players:
            if self.dealtype == "0/54" or self.dealtype == "7/27":
                print(f"{player.name}: Best high = {player.high_score}, Best low = {player.low_score}")
            elif self.dealtype in split_games:
                print(f"{player.name}: Best high = {player.high_hand[0]}, Best low = {player.low_hand[0]}")
            else:
                print(f"{player.name}: Best high = {player.high_hand[0]}")

        self.payout(high_winners, low_winners)


    def payout(self, high_winners, low_winners):
        #possible winner senerios
        if len(high_winners) == 0:
            low_winnings = self.pot / len(low_winners)
            high_winnings = 0
        elif len(low_winners) == 0:
            low_winnings = 0
            high_winnings = self.pot / len(high_winners)
        else:
            low_winnings = (self.pot / 2) / len(low_winners)
            high_winnings = (self.pot / 2) / len(high_winners)

        print()
        print(f"High payout = {high_winnings}, High winners are:")
        for player in high_winners:
            print(f"\t{player.name}")

        print(f"Low payout = {low_winnings}, Low winners are:")
        for player in low_winners:
            print(f"\t{player.name}")
        print("###############################################################")
        print()

        #award people their winnings
        for player in self.players:
            if player in low_winners:
                player.chip_stack += low_winnings
            elif player in high_winners:
                player.chip_stack += high_winnings

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
