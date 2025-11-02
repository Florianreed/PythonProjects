import random
def main():
    level = get_level()
    s = 0
    for _ in range(10):
        x, y = generate_integer(level), generate_integer(level)
        s += score(x, y)
    print(f"score: {s}")
            
    
def get_level():
    while True:
        try:
            lv = int(input("level: "))
            if lv not in [1, 2, 3]:
                raise ValueError
            return lv
        except ValueError:
            pass

def score(x, y):
    e = 0
    s1 = 1
    while True:
        try:
            ans = int(input(f"{x} + {y} = "))
            if ans != x + y:
                raise ValueError
            return s1
        except ValueError:
            print("EEE")
            e += 1
            s1 = 0
            pass
        if e == 3:
            print(f"{x} + {y} = {x + y}")
            return 0



def generate_integer(level):
        return random.randint(10 ** (level - 1), 10 ** (level) - 1)

if __name__ == "__main__":
    main()