import random


def generate_messy_code():
        
    x = random.randint(1, 100)
    y = random.randint(1, 100)
    # this is a useless comment
    if x > y:
        print("x is greater than y")
           
    else:        
        print("y is greater than x")
        # dead code
    z = x * y
    #another useless comment
    return z