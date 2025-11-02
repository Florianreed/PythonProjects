while True:
    try:
        x, y = input("Fraction: ").split("/")
        z = round(int(x) *100 / int(y))
        break
    except (ValueError, ZeroDivisionError):
        pass
if z >= 99:
    print("F")
elif z <= 1:
    print("E")
else:
    print(z, "%", sep="")