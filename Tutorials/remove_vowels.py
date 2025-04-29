def disemvowel(string):
    vowels = 'aeiouAEIOU'
    string_lst = list(string)
    new_lst = [];

    for letter in string_lst:
        if letter not in vowels:
            new_lst.append(letter)
    
    result = "".join(new_lst)
    
    return result;

print(disemvowel("No offense but, Your writing is among the worst I've ever read"));