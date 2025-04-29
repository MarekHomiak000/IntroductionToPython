try:
    num = int(input("number: "))
    def even_odd(num):
        return "even" if num % 2 == 0 else "odd"
    print(f'The number is {even_odd(num)}')
except ValueError:
    print("Zadaj platné číslo!")