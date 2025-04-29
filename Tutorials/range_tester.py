def ret(num):
    return "within 100" if num < 100 else "within 1000" if num < 1000 else "within 2000" if num < 2000 else "above 2000"

text = "cathcatas"
x = text.count("cat"[:])


def multiplicationTable(N):## in is a membership operator that is true if something is a member of sequence
    for i in range(N, 11): ## i in range(x,y,z) means i goes from x to y-1 and increments z steps in each iteration
        print(i * N, end=" ")
multiplicationTable(5)

print(x)