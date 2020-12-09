from game_play import *

#helpfull functions for Game class
class Game_helper:

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
                                self.pot += four_price
                                #increase four_price
                                four_price += 5

                                #give new down card
                                card = self.deck.draw_card()
                                card.type = "down"
                                player.hand.cards.append(card)

                                print(self)
                                four_found = True

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
                            self.pot += four_price
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

        while(1==1):
            if player1.name == winner:
                player1.chip_stack += payout
                player2.chip_stack -= payout
                break
            elif player2.name == winner:
                player1.chip_stack -= payout
                player2.chip_stack += payout
                break
            else:
                print("Enter valid winner name")

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
                    if players_going_high[0] != '':
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
                    if players_going_low[0] != '':
                        for name in players_going_low:
                            if name not in player_names:
                                raise Exception()
                    break
                except:
                    print("Error proccessing players going low")

        # calculate high and low winners
        if self.dealtype == "0/54":

            high_winners, low_winners = determine_winner_0_54(self.players, players_going_high, players_going_low)

            #pig conditions
            for player in self.players:
                if (player.name in players_going_high) and (player.name in players_going_low):
                    #won high but lost low
                    if (player in high_winners) and (player not in low_winners):
                        print(f"{player.name} won high but lost low")
                        players_going_high.remove(player.name)
                    #won low but lost high
                    elif (player in low_winners) and (player not in high_winners):
                        print(f"{player.name} won low but lost high")
                        players_going_low.remove(player.name)
                    high_winners, low_winners = determine_winner_0_54(self.players, players_going_high, players_going_low)

        elif self.dealtype == "7/27":

            high_winners, low_winners = determine_winner_7_27(self.players, players_going_high, players_going_low)

            #pig conditions
            for player in self.players:
                if (player.name in players_going_high) and (player.name in players_going_low):
                    #won high but lost low
                    if (player in high_winners) and (player not in low_winners):
                        print(f"{player.name} won high but lost low")
                        players_going_high.remove(player.name)
                    #won low but lost high
                    elif (player in low_winners) and (player not in high_winners):
                        print(f"{player.name} won low but lost high")
                        players_going_low.remove(player.name)
                    high_winners, low_winners = determine_winner_7_27(self.players, players_going_high, players_going_low)

        elif self.dealtype == "7_card_screw":

            for player in self.players:
                if player.name in players_going_high:
                    determine_hand_high(player, self.table.cards, self.wilds)
                if player.name in players_going_low:
                    determine_hand_low(player, self.table.cards, self.wilds)

            high_winners = calculate_high_winner(self.players, players_going_high)
            low_winners = calculate_low_winner(self.players, players_going_low)

            #pig conditions
            for player in self.players:
                if (player.name in players_going_high) and (player.name in players_going_low):
                    #won high but lost low
                    if (player in high_winners) and (player not in low_winners):
                        print(f"{player.name} won high but lost low")
                        players_going_high.remove(player.name)
                    #won low but lost high
                    elif (player in low_winners) and (player not in high_winners):
                        print(f"{player.name} won low but lost high")
                        players_going_low.remove(player.name)
                    high_winners = calculate_high_winner(self.players, players_going_high)
                    low_winners = calculate_low_winner(self.players, players_going_low)

        elif self.dealtype == "elevator":

            for player in self.players:
                determine_elivator_hands(player, self.table, self.wilds)

            high_winners = calculate_high_winner(self.players, players_going_high)
            low_winners = calculate_low_winner(self.players, players_going_low)

            #pig conditions
            for player in self.players:
                if (player.name in players_going_high) and (player.name in players_going_low):
                    #won high but lost low
                    if (player in high_winners) and (player not in low_winners):
                        print(f"{player.name} won high but lost low")
                        players_going_high.remove(player.name)
                    #won low but lost high
                    elif (player in low_winners) and (player not in high_winners):
                        print(f"{player.name} won low but lost high")
                        players_going_low.remove(player.name)
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

            #pig conditions
            for player in self.players:
                if (player.name in players_going_high) and (player.name in players_going_low):
                    #won high but lost low
                    if (player in high_winners) and (player not in low_winners):
                        print(f"{player.name} won high but lost low")
                        players_going_high.remove(player.name)
                    #won low but lost high
                    elif (player in low_winners) and (player not in high_winners):
                        print(f"{player.name} won low but lost high")
                        players_going_low.remove(player.name)
                    high_winners = calculate_high_winner(self.players, players_going_high)
                    low_winners = calculate_low_winner(self.players, players_going_low)

        elif self.dealtype == "holdem_split":

            for player in self.players:
                determine_omaha_hands(player, self.table, self.wilds)

            high_winners = calculate_high_winner(self.players, players_going_high)
            low_winners = calculate_low_winner(self.players, players_going_low)

            #pig conditions
            for player in self.players:
                if (player.name in players_going_high) and (player.name in players_going_low):
                    #won high but lost low
                    if (player in high_winners) and (player not in low_winners):
                        print(f"{player.name} won high but lost low")
                        players_going_high.remove(player.name)
                    #won low but lost high
                    elif (player in low_winners) and (player not in high_winners):
                        print(f"{player.name} won low but lost high")
                        players_going_low.remove(player.name)
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
            if player in high_winners:
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
                    if float(bet) < 0:
                        raise Exception("Can't raise a negative number")
                    else:
                        bet = current_bet - player.bet + float(bet)

                bet = float(bet)
                #exchange money
                player.chip_stack -= bet
                self.pot += bet

                bet_recorded = True
            except:
                print("error processing bet try again")

        return bet
