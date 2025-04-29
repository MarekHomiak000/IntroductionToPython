import random

def game(number):
    guessed = False
    tries = 10
    
    while not guessed and tries > 0:    
        print("Mas ",tries," pokusov")

        try:
            guess = int(input("Zadaj svoj pokus (1-100): "))
            if guess <= 0 or guess >= 101:
                print("Tvoje cislo je v zlom rozsahu, skus to este raz")
                continue
        except ValueError:
            print("Zadavas neplatne cislo, zadaj cele cislo od 1 po 100, skus to este raz")
            continue

        print("-----------------------")

        if number < guess:
            print("Dobry pokus ale cislo je mensie")
        elif number > guess:
            print("Dobry pokus ale cislo je vacsie")
        else:
            print("*** Popici, vyhral si ***")
            print("Tajomne cislo bolo ", number)
            guessed = True

        tries -= 1
    
    print("\nDosli ti pokusy :(")
        

if __name__ == '__main__':
    random_number = random.randint(0, 101)
    game(random_number)