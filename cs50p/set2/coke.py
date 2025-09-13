def check(n):
    if n in [25, 10, 5]:
        return n
    else:
        return 0
amt = 50
while amt > 0:
    print("Amount due:", amt)
    insert = int(input("Insert Coin:"))
    amt -= check(insert)
print("Change owed:", -amt)