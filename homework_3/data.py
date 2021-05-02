import random
import string

email = "froztgal1996@mail.ru"
password = "actonic1"


def get_random_string(min_len=10, max_len=20):
    name_length = random.randint(min_len, max_len)
    return ''.join(random.choices(string.ascii_letters + string.digits,
                                  k=name_length))
