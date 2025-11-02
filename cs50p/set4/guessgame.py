import random
def main():
    n = get_int("Level: ")
    r = random.randint(1, n)
    while True:
        guess = get_int("Guess: ")
        if guess > r:
            print("Too big")
        elif guess < r:
            print("too small")
        else:
            print("just right")
            break
    
def get_int(prompt):
    while True:
        try:
            if int(input(prompt)) >= 1:
                return int(input(prompt))
        except ValueError:
            pass
main()