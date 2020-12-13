Author - Noah Kruss

Contact info - nkruss@light-waves.net

# Project Description:

A poker gameplay system to host and play a variety of different poker games with others.

Gameplay is located in the poker.py function which the table host will run and screen share. While playing a game all player cards will be displayed, with down card information being encrypted into a three character code before being shown. The encryption makes it so that only the player running card_decryptor.py with the correct "card offset" and "card multiplier" values can get the correct card value relating to the three character code.

## Poker game options

  Seven Card Stud Games
  * Baseball
  * Queens
  * Whores of Chicago
  * Bi-polar
  * David and Goliath

  Community Card Games
  * Texas Holdem
  * Omaha
  * Elevator
  * Kings Corners

  Other Games
  * Nicks Challenge
  * Seven Card Screw Your Neighbor
  * One Card Screw Your Neighbor (Pass the Trash)
  * Zero Fifty-Four
  * Seven Twenty-Seven


## How to host a game

Run poker.py file and screen share the poker.py outputs with the other players. Once file begins running input names of people playing in the game then enter "done". Then send each player privately their "card offset" and "card multiplier" values which can be found in the created player_info.txt file. 

Notes
  * It is the job of the game host running poker.py to input all player actions.

## How to play in a game

Download repository and run card_decryptor.py. Then enter the "card offset" and "card multiplier" values provided by the game host.

Once "card offset" and "card multiplier" are inputted enter cards codes displayed in the table hosts poker.py terminal for your given hand

Card Decryptor Special Commands
  * "next" - Clear current hand of cards
  * "remove" - Remove select card code from hand (card code will be specified by index of the card within the hand)
  * "reorder" - Reorder the cards in hand
  * "quit" - terminate card_decryptor.py

Notes
  * When entering card codes be careful to enter "L" opposed to "l"
  * If you input another player's cards you will get card information back but there is no guarantee that card information is at all accurate

## Additional Notes

Colored cards - Only functional for linux systems. If running repository on a system that is not linux or doesn't run bash you will need to select "n" when asked if you want to use colored cards.

Pig condition  
  * If a person pigs on a hand they will win everything if they win both high and low
  * If the win either high or low and lose the other they get nothing
  * If they win either high or low and tie on the other they will split the half they tied on and take the full half they won
  * If they tie on both high and low they will split both pots
