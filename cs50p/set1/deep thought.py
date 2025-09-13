a = input("What is the Answer to the Great Question of Life, the Universe, and Everything?").casefold()
match a:
    case "42" | "forty-two" | "forty two":
        print("yes")
    case _:
        print("no")