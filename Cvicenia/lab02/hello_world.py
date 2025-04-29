#formatovane vystupy
meno = "Marek"

print("Hello " + meno + "!")
print("Hello", meno)
print(f"Hello {meno}!")

number = 3.121212121
num = number**2

print(num)
print(round(num, 3))
print(int(num))
print(f"{num:.3f}")
print("{:.3f}".format(num))



#parita cisla
num2 = 2
if num2 % 2 == 0:
    print("even")
else:
    print("odd")



#spolocne delitele
cislo1 = 20
cislo2 = 60

if cislo1 < cislo2:
    smaller = cislo1
else:
    smaller = cislo2

for i in range(1, smaller+1):
    if cislo1 % i == 0 and cislo2 % i == 0:
        print(i)



#prvocislo
prvocislo = 7
state = True
for i in range(2, prvocislo):
    if prvocislo % i == 0:
        print("nie je prvocislo")
        state = False
        break
if state:
    print("prvocislo")