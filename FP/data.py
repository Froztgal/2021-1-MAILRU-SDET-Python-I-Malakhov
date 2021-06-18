import random
import string


def get_random_string():
    string_length = random.randint(6, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=string_length))
