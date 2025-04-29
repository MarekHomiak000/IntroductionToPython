def areAnagrams(s1, s2):
    #code here
    if len(s1) != len(s2):
        return False
    summ = 0
    s2 = list(s2)
    for i in s1:
        if i in s2:
            s2.remove(i)
        else:
            return False
        
    return not s2

print(areAnagrams("helloooo", "oooelhlo"))  
print(areAnagrams("hello", "world"))        
print(areAnagrams("listen", "silent"))  