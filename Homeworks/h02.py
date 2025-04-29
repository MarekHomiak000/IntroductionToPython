num1 = 20
num2 = 5

def common_divisors1(num1, num2):
    lowest = min(num1, num2)
    sum = 0
    for i in range(1, lowest + 1):
        if num2 % i == 0 and num1 % i == 0:
            sum += i
    return sum

def common_divisors2(num1, num2):
    sum = 0
    while num2 != 0:
        temp = num2
        num2 = num1 % num2 
        num1 = temp
    
    for i in range(1, num1 + 1):
        if num1 % i == 0:
            sum += i
    return sum


print(common_divisors1(num1, num2))
print(common_divisors2(num1, num2))