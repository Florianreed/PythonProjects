dic = {}
while True:
    try:
        item = input().upper()
        if item in dic:
            dic[item] += 1
        else:
            dic[item] = 1
    except EOFError:
        break
    
for i in dic:
    print(dic[i], i)