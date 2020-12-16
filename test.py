import math


def lcm(a, b):
    return (a * b) // math.gcd(a, b)


l = lcm(16, 32)
print(l)
a = list()


def to_2(x):
    n = ""
    while x > 0:
        y = str(x % 2)
        n = y + n
        x = int(x / 2)
    if n[-4:-1] != '000':
        return True
    else:
        return False


for i in range(3721, 7753):
    count = 0
    for j in range(len(str(i))):
        count += int(str(i)[j])
    if count % 3 == 0:
        if to_2(i):
            a.append(i)

print((len(a), min(a)))
