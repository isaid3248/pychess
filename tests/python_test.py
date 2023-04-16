def gcd(x,y ):
    if(y == 0):
        return x
    else:
        return gcd(y, x % y)

out = []
for i in range(200):
    if gcd(200, i) != 1:
        out.append(i)

print(len(out))
for i in range(200):