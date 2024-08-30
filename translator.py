import argparse
import re
def translate(string):
    braille_pattern=r"^[O.]"
    english_pattern=r"^[A-Za-z0-9]"
    if re.match(english_pattern,string):
        print("Input is English")
    else:
        print("input is Braille")
def main():
    parser=argparse.ArgumentParser(description="English To Braille and Vice-Versa")
    parser.add_argument("input",type=str,help="Input String")
    args_obj=parser.parse_args()
    translate(args_obj.input)
if __name__=="__main__":
    main()