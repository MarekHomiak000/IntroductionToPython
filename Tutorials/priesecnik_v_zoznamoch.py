arr1 = [1, 2, 3]
arr2 = [1, 2, 3, 4, 5]

def intersection(arr1, arr2):
    # Nájdeme priesečník dvoch zoznamov
    c = list(set(arr1) & set(arr2))
    # Zoradíme výsledný zoznam
    return sorted(c)


print(intersection(arr1, arr2))