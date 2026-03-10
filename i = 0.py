import random
list = []
for i in range(0, 100):
    list.append(random.randint(-500, 100))
n = len(list)
jah = True
for kordus in range(n):
    i = -2
    d = -1
    while d > -n:
        if list[i] < list[d]:
            i1 = list[i]
            list[i] = list[d]
            list[d] = i1
        i += -1
        d += -1
print(str(list))