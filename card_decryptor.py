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
    if len(code)==3:
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
        print("Please type in the codes of the cards you want decoded.")
        print("Input each card one at a time. Type 'next' to move to next hand inputting cards. Type 'quit' to quit.")

        while(1):
            inCode = input("Enter the card codes seperated by ' ':  ")
            if inCode == 'next':
                print('\n' for _ in range(10))
                break
            elif inCode == 'quit':
                quit()
            else:
                codes = inCode.split(' ')
                decryptor(base_deck, card_offset, inverse, codes)

main()
