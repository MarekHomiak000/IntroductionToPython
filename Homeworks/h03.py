# Meno: Homiak, Marek
# Spolupráca: 
# Použité zdroje: 
# Čas: 

# Podrobný popis je dostupný na: https://github.com/ianmagyar/introduction-to-python/blob/master/assignments/homeworks/homework03.md

# Hodnotenie: /1b

import random
import string

# 17. Máme zoznam reťazcov lst. Pomocou list comprehension vygenerujte zoznam lst2,
# ktorý bude obsahovať iba tie prvky zoznamu lst, ktoré začínajú na písmeno s.
lst = [''.join(random.choices(string.ascii_lowercase, k=6)) for _ in range(20)]
print(lst)
lst2 = [s for s in lst if s[0] == 's']
print(lst2)
print("------------")


# 13. Máme zoznam reťazcov lst. Pomocou list comprehension vygenerujte zoznam lst2,
# ktorý bude obsahovať iba tie prvky zoznamu lst, ktoré obsahujú písmeno a
# alebo písmeno e.
lst = [''.join(random.choices(string.ascii_lowercase, k=6)) for _ in range(20)]
print(lst)
lst2 = [word for word in lst if 'a' in word or 'e' in word]
print(lst2)
print("------------")

# --------------------
# Úloha 2

# 37. Máme zoznam náhodných reťazcov lst. Upravte zoznam pomocou
# lambda výrazu tak, že vymažete posledné písmeno každého reťazca.
lst = [''.join(random.choices(string.ascii_lowercase, k=6)) for _ in range(20)]
print(lst)
edited_list = list(map(lambda x: x[:-1], lst))
print(edited_list)

