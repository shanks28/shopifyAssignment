import argparse
import re
def translate(string="Abc 123"):
    braille_pattern=r"^[O.]"
    english_pattern=r"^[A-Za-z0-9]-[O]"
    float_pattern = r'[-+]?\d*\.\d+'
    braille_alphabet_and_special_characters = {
        "A": "O.....",
        "B": "O.O...",
        "C": "OO....",
        "D": "OO.O..",
        "E": "O..O..",
        "F": "OOO...",
        "G": "OOOO..",
        "H": "O.OO..",
        "I": ".OO...",
        "J": ".OOO..",
        "K": "O...O.",
        "L": "O.O.O.",
        "M": "OO..O.",
        "N": "OO.OO.",
        "O": "O..OO.",
        "P": "OOO.O.",
        "Q": "OOOOO.",
        "R": "O.OOO.",
        "S": ".OO.O.",
        "T": ".OOOO.",
        "U": "O...OO",
        "V": "O.O.OO",
        "W": ".OOO.O",
        "X": "OO..OO",
        "Y": "OO.OOO",
        "Z": "O..OOO",
        "1": "O.....",
        "2": "O.O...",
        "3": "OO....",
        "4": "OO.O..",
        "5": "O..O..",
        "6": "OOO...",
        "7": "OOOO..",
        "8": "O.OO..",
        "9": ".OO...",
        "0": ".OOO..",
        ".": "..OO.O",
        ",": "..O...",
        "?": "..O.OO",
        "!": "..OOO.",
        ":": "..OO..",
        ";": "..O.O.",
        "-": "..O..O",
        "/": "..O..O",
        "<": ".O.O..",
        ">": ".O..O.",
        "(": ".O..OO",
        ")": ".O.OO.",
        "capital follows": ".....O",
        "decimal follows": ".O...O",  # Corrected representation
        "number follows": ".O.OOO",
        " ": "......"
    }
    res=""
    to_continue=0
    number_flag=0
    decimal_flag=0
    match=re.search(float_pattern,string)
    position=match.start() if match else len(string)
    braille_to_english = {
        'O.....': 'a', 'O.O...': 'b', 'OO....': 'c', 'OO.O..': 'd', 'O..O..': 'e',
        'OOO...': 'f', 'OOOO..': 'g', 'O.OO..': 'h', '.OO...': 'i', '.OOO..': 'j',
        'O...O.': 'k', 'O.O.O.': 'l', 'OO..O.': 'm', 'OO.OO.': 'n', 'O..OO.': 'o',
        'OOO.O.': 'p', 'OOOOO.': 'q', 'O.OOO.': 'r', '.OO.O.': 's', '.OOOO.': 't',
        'O...OO': 'u', 'O.O.OO': 'v', '.OOO.O': 'w', 'OO..OO': 'x', 'OO.OOO': 'y',
        'O..OOO': 'z', '..OO.O': '.', '..O...': ',', '..O.OO': '?', '..OOO.': '!',
        '..OO..': ':', '..O.O.': ';', '..O..O': '/', '.O.O..': '<', '.O..O.': '>',
        '.O..OO': '(', '.O.OO.': ')', '.....O': 'capital follows', '.O...O': 'decimal follows',
        '.O.OOO': 'number follows', '......': 'space'
    }
    if re.match(english_pattern,string):
        print("english mode")
        for index,value in enumerate(string):
            if value.isalpha() and value .isupper():
                res+=braille_alphabet_and_special_characters['capital follows']
                res+=braille_alphabet_and_special_characters[value]
            elif value.isalpha() and value .islower():
                value=value.upper()
                res+=braille_alphabet_and_special_characters[value]
            elif ord(value) in range(48,58) and not match:
                res+=braille_alphabet_and_special_characters['number follows']
                res+=braille_alphabet_and_special_characters[value]
                to_continue=index+1
                number_flag=1
                break
            elif value.isspace():
                res+=braille_alphabet_and_special_characters[' ']
        while to_continue < len(string) and number_flag==1: # there could be letters after an integer
            if string[to_continue].isdigit():
                res += braille_alphabet_and_special_characters[string[to_continue]]
            elif string[to_continue].isupper():
                res += braille_alphabet_and_special_characters['capital follows']
                res += braille_alphabet_and_special_characters[string[to_continue]]
            elif string[to_continue].isspace():
                res+=braille_alphabet_and_special_characters[' ']
            elif string[to_continue].isalpha() and string[to_continue] .islower():
                value=string[to_continue].upper()
                res+=braille_alphabet_and_special_characters[value]
            to_continue+=1
        while match and position<len(string):
            if decimal_flag==0:
                res+=braille_alphabet_and_special_characters['decimal follows']
            if string[position]!='.':
                res+=braille_alphabet_and_special_characters[string[position]]
            position+=1
            decimal_flag=1
        print(res)
    else: # input length will be multiples of 6
        res=""
        print("braille mode")
        capital_flag=0
        number_flag=0
        decimal_flag=0
        for i in range(0,len(string),6):
            braille_character=string[i:i+6]
            if braille_to_english[braille_character]=="capital follows":
                capital_flag=1
            elif braille_to_english[braille_character]=="number follows":
                number_flag=1
            elif braille_to_english[braille_character]==" ":
                capital_flag=0 # reset all flags for a potential new  type of word
                res+=" "
                number_flag=0
                decimal_flag=0
            elif capital_flag==1:
                print(braille_to_english[braille_character])
                res+=braille_to_english[braille_character]
                print(res)
                capital_flag=0 # only following character to be capitalized
            elif number_flag==1:
                res+=braille_to_english[braille_character]
            elif braille_to_english[braille_character]=='decimal follows':
                decimal_flag=1
            elif decimal_flag==1:
                res+=braille_to_english[braille_character]+'.'
                number_flag=1 # after the first decimal all other characters are treated as numbres
                decimal_flag=0
            else:
                res+=braille_to_english[braille_character].lower()
        print(res)
def main():
    parser=argparse.ArgumentParser(description="English To Braille and Vice-Versa")
    parser.add_argument("input",type=str,help="Input String")
    args_obj=parser.parse_args()
    translate(args_obj.input)
if __name__=="__main__":
    if ".....OO.....O.O...OO...........O.OOOO.....O.O...OO..........OO..OO.....OOO.OOOO..OOO"==".....OO.....O.O...OO...........O.OOOO.....O.O...OO..........OO..OO.....OOO.OOOO..OOO":
        print("yes")
    else:
        print("no")
    main()