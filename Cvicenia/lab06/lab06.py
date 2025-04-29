import random
import os

def load_words(dataset_path):
    try:
        my_file = open(dataset_path, "r")
    except FileNotFoundError:
        print("no file")
        return []
    
    words = []
    for line in my_file.readlines():
        try:
            if len(line) == 6:
                word = line[:-1]
                if word.isalpha():
                    words.append(word.lower())
                else:
                    raise ValueError("word contains nono-letter char")
        except ValueError:
            pass
    return words


def get_puzzle(word_list):
    return random.choice(word_list)


def is_game_finished(guess, puzzle):
    return guess.lower() == puzzle.lower()


def evaluate_guess(guess, puzzle):
    result = []
    guess = guess.lower()

    for i, let in enumerate(guess):
        letter_info = (let, let in puzzle, let == puzzle[i])
        result.append(letter_info)


    return result


def start_game(dataset_path):
    #nacitanie slov
    words_list = load_words(path)

    #nahodne slovo
    puzzle = get_puzzle(words_list)
    guess = input("zadajte slovo: ")

    x = 0
    while not is_game_finished(guess, puzzle) or x <= 5:
        if guess.lower() not in words_list:
            print("neplatne slovo")
            continue
        else:
            print(evaluate_guess(guess, puzzle))
            x += 1

        guess = input("zadajte slovo: ")


    
    if(x == 6):
        print("u lost")
    else:
        print("u won")

if __name__ == '__main__':
    #start_game("word_list.txt")
    path = os.path.join(os.path.dirname(__file__), "word_list.txt")
    start_game(path)
