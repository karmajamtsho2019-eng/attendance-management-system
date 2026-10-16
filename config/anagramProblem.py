from collections import Counter

def are_anagrams(s1, s2):
    return Counter(s1) == Counter(s2)

string1 = input("Enter the first string: ")
string2 = input("Enter the second string: ")

if are_anagrams(string1, string2):
    print("Result: True (They are anagrams!)")
else:
    print("Result: False (They are NOT anagrams.)")