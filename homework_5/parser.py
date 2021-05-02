import re
import sys
import json


def top_n_keys(dictionary, top):
    n = 0
    new_dict = {}
    sorted_keys = list(dictionary.keys())
    sorted_keys.sort(reverse=True)
    for i in sorted_keys:
        new_dict[i] = dictionary[i]
        n += 1
        if n == top:
            return new_dict


def top_n_values(dictionary, top):
    n = 0
    new_dict = {}
    sorted_dict = dict(sorted(((value, key) for (key, value) in dictionary.items()), reverse=True))
    for k, v in sorted_dict.items():
        new_dict[k] = v
        n += 1
        if n == top:
            return new_dict


format = re.compile(r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} ([+\-])\d{4})] ((\"(?P<method>.+) )(?P<url>.+)(http\/[1-2]\.[0-9]")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""", re.IGNORECASE)

num_req = 0
dict_common = {}
dict_freq = {}
dict_4xx = {}
dict_5xx = {}

with open('access.log', 'r') as f:
    for line in f:
        # Подсчет общего количества запросов в файле
        num_req += 1

        data = re.search(format, line)
        if data:
            datadict = data.groupdict()

        # Подсчет общего количества запросов в файле по типу
        if datadict["method"] in dict_common:
            dict_common[datadict["method"]] += 1
        else:
            dict_common[datadict["method"]] = 1

        # Подсчет топ 10 самых частых запросов
        if datadict["url"] in dict_freq:
            dict_freq[datadict["url"]] += 1
        else:
            dict_freq[datadict["url"]] = 1

        # Подсчет топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой
        # надо продумать как сортировать? помоему что-то ту не так
        if '400' <= datadict['statuscode'] < '500':
            if datadict["bytessent"] in dict_4xx:
                pass
            else:
                dict_4xx[datadict["bytessent"]] = [datadict["url"], datadict["ipaddress"], datadict["statuscode"]]

        # Подсчет топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой
        if datadict['statuscode'] >= '500':
            if datadict["ipaddress"] in dict_5xx:
                dict_5xx[datadict["ipaddress"]] += 1
            else:
                dict_5xx[datadict["ipaddress"]] = 1

    dict_freq = top_n_values(dict_freq, 10)
    dict_4xx = top_n_keys(dict_4xx, 5)
    dict_5xx = top_n_values(dict_5xx, 5)

    with open('result_python.txt', 'w') as rf:
        rf.write('1 -- Общее количество запросов' + '\n')
        rf.write(str(num_req) + '\n')
        rf.write('2 -- Общее количество запросов по типу, например: GET - 20, POST - 10 и т.д.' + '\n')
        rf.write(str(dict_common) + '\n')
        rf.write('3 -- Топ 10 самых частых запросов' + '\n')
        rf.write(str(dict_freq) + '\n')
        rf.write('4 -- Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой' + '\n')
        rf.write(str(dict_4xx) + '\n')
        rf.write('Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой' + '\n')
        rf.write(str(dict_5xx) + '\n')

    if '--json' in sys.argv:
        with open('result_python_json.json', 'w') as rfj:
            dict_json = {1: num_req, 2: dict_common, 3: dict_freq, 4: dict_4xx, 5: dict_5xx}
            json.dump(dict_json, rfj)
