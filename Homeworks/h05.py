# Meno: Homiak, Marek
# Spolupráca: 
# Použité zdroje: 
# Čas: 

# Podrobný popis je dostupný na: https://github.com/ianmagyar/introduction-to-python/blob/master/homeworks/homework05.md

# Hodnotenie: /1b

# 13
def is_triangle(side_a = None, side_b = None, side_c = None):                       #zmena na None aby som mohol kontrolovat ci su zadane vsetky parametra
    # checks if three numbers can represent the sides of a valid triangle
    # inputs should be positive numbers

    #kontrola vsetkych parametrov
    if side_a is None or side_b is None or side_c is None:
        raise TypeError("Function expects 3 parameters")

    #kontrola ci sa daju scitat
    try:
        side_a, side_b, side_c = float(side_a), float(side_b), float(side_c)
    except ValueError:
        raise ValueError("You are trying to enter wrong types")
    else:
        print("Correct types")

    #kontrola ci su vacsie ako 0
    if side_a <= 0 or side_b <= 0 or side_c <= 0:
        raise ValueError("Sides of triangle must be positive numbers")

    # TODO: check the validity of input - are all sides positive numbers?
    if side_a + side_b < side_c:
        return False
    if side_a + side_c < side_b:
        return False
    if side_b + side_c < side_a:
        return False

    return True

print(is_triangle(3, 4, 5))      # True (platný trojuholník)
print(is_triangle("0.9", 2, 3))  # True (platný trojuholník s float konverziou)
print(is_triangle(1, 2, 3))      # False (neplatný trojuholník)
print(is_triangle(-1, 2, 3))     # Chyba (záporná strana)
print(is_triangle(0, 2, 3))      # Chyba (nulová strana)
print(is_triangle("a", 2, 3))    # Chyba (nesprávny typ)
print(is_triangle("1", 2))       # Chyba (chýbajúci parameter)