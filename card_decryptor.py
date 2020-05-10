from cards_deck import *

def decryptor(base_deck, card_offset, inverse, code):

    from_base_36 = {"0":0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9,
                    "a":10, "b":11, "c":12, "d":13, "e":14, "f":15, "g":16, "h":17, "i":18, "j":19,
                    "k":20, "l":21, "m":22, "n":23, "o":24, "p":25, "q":26, "r":27, "s":28, "t":29,
                    "u":30, "v":31, "w":32, "x":33, "y":34, "z":35}

    first_char = from_base_36[code[0]]
    second_char = from_base_36[code[1]]
    third_char = from_base_36[code[2]]

    card_code = (first_char * (36 ** 2)) + (second_char * 36) + third_char

    card_code = ((card_code * inverse - card_offset) % 46133) % 52

    card = base_deck.cards[card_code]
    print(ascii_version_of_card(card))

def is_valid(code):
    valid = True

    #check code legth
    if len(code) != 3:
        print("code length error")
        valid = False

    valid_characters = ["0","1","2","3","4","5","6","7","8","9",
                        "a","b","c","d","e","f","g","h","i","j","k",
                        "l","m","n","o","p","q","r","s","t","u","v",
                        "w","x","y","z"]

    for char in code:
        if char not in valid_characters:
            print(f"{char} is an invalid character")
            valid = False

    return valid

def main():
    print("Make sure to be careful with initial inputs! :)")

    #get card offset inputed corectly
    offset_inputted = False
    while(offset_inputted == False):
        try:
            card_offset = int(input("Enter your card_offset value:  "))
            if ((card_offset < 0) or (card_offset > 46132)):
                pass
            else:
                offset_inputted = True
        except:
            print("Invalid card_offset")

    multiplier_inputted = False
    while(multiplier_inputted == False):
        try:
            card_multiplier = int(input("Enter your card_multiplier value:  "))
            if ((card_multiplier < 1) or (card_multiplier > 46132)):
                pass
            else:
                multiplier_inputted = True
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

    while(1==1):
        print("Please type in the codes of the cards you want decoded.")
        print("Input each card one at a time. Type 'next' to move to next hand inputting cards. Type 'quit' to quit.")

        codes_inputted = False
        while(codes_inputted == False):
            code = input("Enter the card code:  ")
            if code == 'next':
                for i in range(20):
                    print()
                codes_inputted = True
            elif code == 'quit':
                quit()
            else:
                if is_valid(code):
                    decryptor(base_deck, card_offset, inverse, code)
                else:
                    print("invalid code input")

main()
