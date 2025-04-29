def to_uppercase(text:str)->str:
    if not isinstance(text,str):
        raise ValueError("input must be a string")
    return text.upper()

output=to_uppercase('appu')
print(output)