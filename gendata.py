import random

def datagen(citySize, seed,min,max):
    items = []
    citys = {}
    random.seed(seed)
    i = 0
    while i < citySize:
        z = random.randint(min,max)
        k = random.randint(min,max)
        a = (z , k)

        if a not in citys:
            citys[i] = {
             "coord" : a
            }
            i += 1

    return citys

