import random


def random_code_generator():
    while True:
        yield random.randint(1000, 9999)




