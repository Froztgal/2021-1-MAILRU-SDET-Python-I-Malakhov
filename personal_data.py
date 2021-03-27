import random
import string

# TODO: Insert your login data here.
email = ""
password = ""

first_names = ["Филипп", "Василий", "Пётр"]
second_names = ["Панкратов", "Петров", "Иванов"]
surnames = ["Ильич", "Сергеевич", "Пашаевич"]

domains = ["@gmail.com", "@mail.ru", "@yandex.ru"]


def get_random_fio():
    return random.choice(second_names) + " " + random.choice(first_names) + " " + random.choice(surnames)


def get_random_email():
    email_length = random.randint(6, 15)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=email_length)) +\
           domains[random.randint(0, len(domains) - 1)]

def get_random_phone():
    return "+7" + ''.join([str(random.randint(0, 9)) for i in range(10)])
