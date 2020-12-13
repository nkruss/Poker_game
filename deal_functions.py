from game_play import *

#Game class deal functions
class Deals:

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
        self.players = players_original[self.dealer_i:] + players_original[:self.dealer_i]
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
                        player_challenging = input(f"{player.name} are you in challenging {player_in_name} y/n? (You have {player.legs} legs)  ")
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
        self.players = players_original[self.dealer_i:] + players_original[:self.dealer_i]

        #create a dictonary of the players where the player's name is the key
        #and the key value is whether or not the player is still in
        player_dic = {}
        for player in self.players:
            player_dic[player.name] = True

        stack_num = input("How many stacks of 5 chips are each person going to start with?  ")
        self.pot = (int(stack_num) * 5) * len(self.players)
        for player in self.players:
            player.chip_stack -= (int(stack_num) * 5)
            player.legs = int(stack_num)

        while(len(self.players) != 1):

            #reset deck if not enough cards
            if len(self.deck.cards) < len(self.players) + 1:
                input("\n##########\n### New Deck ###\n##########")
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
        self.players = players_original[self.dealer_i:] + players_original[:self.dealer_i]

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
            for i in range(3):
                self.deal_down(display=False)

            #print player hands
            string = ''
            for player in self.players:
                string += player.coded_str_player(self.deck.deck_code, self.card_color)
            print(string)
            print(self)

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
            self.reveal_all_hands()
            for card in self.table.cards:
                card.type = "up"
            print(self)

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

                all_passed = True
                for player in eligible_players:
                    # if player in eligible_players:
                    hit = input(f"{player.name} (you have {3 - player.legs} passes left) do you want another card y/n?  ")
                    if hit == "y":
                        card = self.deck.draw_card()
                        player.hand.add_up_card(card)
                        all_passed = False
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
                if len(eligible_players) == 0 or all_passed == True:
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
