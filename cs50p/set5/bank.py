def value(greet):
    if greet[:5] == "hello":
        return 0
    elif greet[0] == "h":
        return 20
    else:
        return 100
    
s = input("greeting: ")
print(f"${value(s)}")