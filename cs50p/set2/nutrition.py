fruit = input("Item: ").casefold()
dic = {
    "apple": 150,
    "avocado": 50,
    "sweet cherries": 100,
}
if fruit in dic:
    print("Calories:", dic[fruit])