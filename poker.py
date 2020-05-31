import random
from game_play import *
from player_class import *
from hand_class import *
from cards_deck import *

def main():
    starting_chip_stack = int(input("Enter starting chip stack amount: "))
    auntie = int(input("Enter auntie amount for games: "))

    #set up players
    players = []
    player_info = open('player_info.txt', 'w')
    player_info.close()
    # players.append(Player("Noah"))
    # players.append(Player("Tova"))
    # players.append(Player("Alex"))
    # players.append(Player("Steve"))
    while(1==1):
        player_name = input("Enter player name (type done to move on):  ")
        if player_name == "done":
            break
        players.append(Player(player_name, starting_chip_stack))

    dealer_i =  0
    while(1==1):
        print()
        print(f"New game, {players[dealer_i].name} is dealer")
        for player in players:
            player.hand.reset()
            print(player)

        print("What game should we play? Type 'game over' to end, 'remove player' to remove a player.")
        gametype = input("Game Options: Baseball, Nicks, Queens, Whores, Texas, Omaha, 0/54, 7_card_screw, Elevator, 1_card_screw, D_and_G:  ")
        games = ["Baseball", "Queens", "Whores", "Nicks", "Texas", "Omaha", "test", "0/54", "7_card_screw", "Elevator", "1_card_screw", "D_and_G"]

        if gametype == "game over":
            break

        elif gametype == "remove player":
            name = input("What is the name of the player to remove?  ")
            for player in players:
                if player.name == name:
                    players.remove(player)

        elif gametype == "add player":
            name = input("Enter plyer name:  ")
            players.append(Player(name))

        elif gametype not in games:
            print("\nPlease enter a valid game\n\n\n")
            pass

        else:
            game = Game(gametype, players, dealer_i, auntie)
            game.play()

            dealer_i += 1

            #loop the dealer
            if dealer_i > len(players)-1:
                dealer_i = 0

        #reset players hands and bet amount
        for player in players:
            player.hand.reset()
            player.bet = 0



main()
