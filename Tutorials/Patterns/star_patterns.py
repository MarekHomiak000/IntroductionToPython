size = 5

def basic_triangle():
    for i in range(1, size+1):
        for j in range(1, i+1):
            print("* ", end=" ")
        print()

def reverse_triangle():
    for i in range(1, size+1):
        for j in range(i, size+1):
           print("* ", end=" ")
        print()

def back_triangle():
    for i in range(1, size+1):
        for j in range(1, size+1):
            print("* ", end=" ")
        print()
 

basic_triangle()
print()
reverse_triangle()
print()
back_triangle()