
    
def validateYPS(string):
    year = string[:4] in range(1900,2100)
    pin = string[4:7] in getPINlist()
    gender = string[-1] in ['M','F'] 
