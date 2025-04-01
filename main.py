from enum import Enum
import random
from collections import defaultdict
import os

IS_DEBUG = os.getenv('DEBUG') == "1"

# Define all the colors used in the game map
class Color(Enum):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"
    PURPLE = "PURPLE"
    BLUE = "BLUE"
    WHITE = "WHITE"

    @property
    def char(self):
        return self.value[0]
    
    @property
    def display(self):
        color_to_emoji = {
            self.RED: '😡',
            self.YELLOW: '😉',
            self.GREEN: '🤢',
            self.PURPLE: '🌚',
            self.BLUE: '🥶',
            self.WHITE: '☁️',
        }
        return color_to_emoji[self]
    
    @classmethod
    def from_char(cls, input_character):
        char_to_color_dict = { color.char: color for color in Color }
        return char_to_color_dict[input_character]

class ResultColor(Enum):
    BLACK = "BLACK"
    WHITE = "WHITE"

    @property
    def display(self):
        result_to_emoji = {
            self.BLACK: '💘',
            self.WHITE: '💔'
        }
        return result_to_emoji[self]
        

class Mastermind:
    secret: list[Color]

    def _generate_secret(self):
        self.secret = random.choices(list(Color), k=4)

    @staticmethod
    def score(guess_colors, secret_colors) -> list[ResultColor]:
        wrong_positions_count = defaultdict(int)
        result = []
        for g, s in zip(guess_colors, secret_colors):
            if g == s:
                result.append(ResultColor.BLACK)
            else:
                wrong_positions_count[s] += 1
        for g, s in zip(guess_colors, secret_colors):
            if g != s:
                if wrong_positions_count[g]:
                    wrong_positions_count[g] -= 1
                    result.append(ResultColor.WHITE)
        return result

    @staticmethod
    def _print_start():
        print("😎 Welcome to EMOJI MASTERMIND! 😎")
        print()
        print("Possible Colors (use first letter):")
        print("  ".join(color.char for color in Color))
        print(" ".join(color.display for color in Color))
        print()
        print("Keep guessing till you win:")
        print()
        print()

    @staticmethod
    def _print_formatted_result(result):
        print("RESULT: " + " ".join(str(result.display) for result in result))

    def play(self):
        # first, generate the secret
        self._generate_secret()
        
        if (IS_DEBUG):
            print("Secret: " + " ".join(sec.char for sec in self.secret))
    
        # print instructions for the user
        self._print_start()
     
        while True:
            # accept player guess
            current_input = input().upper()
            current_input_list = current_input.split(' ')
            current_input_colors = [ Color.from_char(input_character) for input_character in current_input_list ]

            # show the user's guess as colors
            print("GUESS:  " + " ".join(c.display for c in current_input_colors))

            # get the score
            result = self.score(current_input_colors, self.secret)
            self._print_formatted_result(result)
            print()

            # check if won, break if so
            if (result == [ResultColor.BLACK]*4):
                print("WOW: YOU WIN 😎")
                print("You are a genius and a scholar 🙏")
                print("Please collect your trophy before you go: 🏆")
                break

def main():
    m = Mastermind()
    m.play()

if __name__ == "__main__":
    main()
