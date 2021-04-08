import random
import string

email = "froztgal1996@mail.ru"
password = "actonic1"


def get_random_name():
    name_length = random.randint(20, 50)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=name_length))
