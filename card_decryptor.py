from cards_deck import *
import os
letters = '0123456789abcdefghijkLmnopqrstuvwxyz'

def decryptor(base_deck, card_offset, inverse, codes, card_color):
    cards = []
    for code in codes:
        charNums = [letters.find(c) for c in code]
        card_code = sum([(n*(36**(2-i))) for i, n in enumerate(charNums)])
        card_code = ((card_code * inverse - card_offset) % 46133) % 52
        cards.append(base_deck.cards[card_code])
    print(ascii_version_of_hand(cards, card_color=card_color))

def validate(code):
    valid = True
    if len(code) != 3:
        valid = False

    for char in code:
        if char not in letters:
            valid = False

    return valid

def main():
    print("Make sure to be careful with initial inputs! :)")

    #get card offset inputed corectly
    while(1):
        try:
            card_offset = int(input("Enter your card_offset value:  "))
            if ((card_offset < 0) or (card_offset > 46132)):
                pass
            else:
                break
        except:
            print("Invalid card_offset")

    while(1==1):
        try:
            card_multiplier = int(input("Enter your card_multiplier value:  "))
            if ((card_multiplier < 1) or (card_multiplier > 46132)):
                pass
            else:
                break
        except:
            print("Invalid card_multiplier")

    card_color = input("Do you want your hand to use colored cards? y/n:  ")
    if card_color == "y":
        card_color = True
    else:
        card_color = False

    base_deck = Deck()

    #Find the multiplicative inverse of card_multiplier (exact code):
    remainder = card_multiplier
    inverse = 1
    temp_inverse = 1
    while (remainder != 1):
        temp_inverse = 46133 // remainder + 1
        inverse = (inverse * temp_inverse) % 46133
        remainder = (remainder * temp_inverse) % 46133

    while(1):
        print("\nPlease type in the codes of the cards you want decoded. Until you start a new had each new code will be added to the current hand")
        print(" Type 'next' to move to next hand inputting cards")
        print(" Type 'remove' to remove codes from current hand")
        print(" Type 'reorder' to reorder the cards in your current hand")
        print(" Type 'quit' to quit")

        current_hand_codes = []
        while(1):
            inCode = input("\nEnter card code (to enter multiple codes seperate them by ' '):  ")

            if inCode == 'next':
                current_hand_codes = []
                os.system('clear')
                break

            elif inCode == 'quit':
                quit()

            elif inCode == 'remove':
                cards_to_remove = input(" Enter index of cards to remove (to enter multiple codes seperate them by ' '):  ")
                try:
                    cards_to_remove = cards_to_remove.split(' ')

                    #shift to zero indexed
                    for index_i in range(len(cards_to_remove)):
                        cards_to_remove[index_i] = int(cards_to_remove[index_i]) - 1

                    counter = 0
                    for card_i in cards_to_remove:
                        cards_to_remove[counter] = current_hand_codes[card_i]
                        counter += 1

                    for code in cards_to_remove:
                        current_hand_codes.remove(code)
                except:
                    print("error discarding try again")

                print(current_hand_codes)

            elif inCode == 'reorder':
                try:
                    print(" Example reorder: 1 5 3 2 4")
                    order_list = input(f" Enter index order you want your hand (seperate card index by ' ')?  ")

                    order_list = order_list.split(' ')

                    #check to make sure corrent number of cards was inputed if
                    ##not create error to get to except statement
                    if len(order_list) != len(current_hand_codes):
                         raise Exception()

                    #shift to zero indexed
                    for index_i in range(len(order_list)):
                        order_list[index_i] = int(order_list[index_i]) - 1

                    reordered_hand = []
                    for index in order_list:
                        reordered_hand.append(current_hand_codes[index])
                    current_hand_codes = reordered_hand

                    print(current_hand_codes)
                    decryptor(base_deck, card_offset, inverse, current_hand_codes, card_color)

                except:
                    print("Error processing inputed reorder")

            else:
                new_codes = inCode.split(' ')

                #remove invalid card codes from hand
                invalid_codes = []
                for code in new_codes:
                    if validate(code) == False:
                        invalid_codes.append(code)
                        print(f"{code} was an invalid card code")
                for code in invalid_codes:
                    new_codes.remove(code)

                current_hand_codes = current_hand_codes + new_codes
                print(current_hand_codes)
                decryptor(base_deck, card_offset, inverse, current_hand_codes, card_color)

main()
