def replace_successive(s):
    if not s:
        return ""
    
    result = [s[0]]
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            result.append('*')
        else:
            result.append(s[i])
            
    return "".join(result)

user_input = input("Enter a string: ")

output = replace_successive(user_input)
print(f"Result: {output}")