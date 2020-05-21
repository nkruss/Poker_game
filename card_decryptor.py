from cards_deck import *
letters = '0123456789abcdefghijkLmnopqrstuvwxyz'

def decryptor(base_deck, card_offset, inverse, codes):
    cards = []
    for code in codes:
        if validate(code):
            charNums = [letters.find(c) for c in code]
            card_code = sum([(n*(36**(2-i))) for i, n in enumerate(charNums)])
            card_code = ((card_code * inverse - card_offset) % 46133) % 52
            cards.append(base_deck.cards[card_code])
        else:
            print('invalid input')
            break
    print(ascii_version_of_hand(cards))

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
        print("Please type in the codes of the cards you want decoded. Untill you start a new had each new code will be added to the current hand")
        print("Type 'next' to move to next hand inputting cards. Type 'quit' to quit.")

        current_hand_codes = []
        while(1):
            inCode = input("Enter card code (to enter multiple codes seperate them by ' '):  ")
            if inCode == 'next':
                for i in range(10):
                    print('\n')
                current_hand_codes = []
                break
            elif inCode == 'quit':
                quit()
            else:
                new_codes = inCode.split(' ')
                current_hand_codes = current_hand_codes + new_codes
                print(current_hand_codes)
                decryptor(base_deck, card_offset, inverse, current_hand_codes)

main()
