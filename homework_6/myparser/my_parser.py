import re
import os


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


def get_results():
    format_str = re.compile(r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} ([+\-])\d{4})] ((\"(?P<method>.+) )(?P<url>.+)(http\/[1-2]\.[0-9]")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""", re.IGNORECASE)

    num_req = 0
    dict_common = {}
    dict_freq = {}
    dict_4xx = {}
    dict_5xx = {}

    with open(os.path.join(os.getcwd(), 'homework_6', 'myparser', 'access.log'), 'r') as f:
        for line in f:
            # Подсчет общего количества запросов в файле
            num_req += 1

            data = re.search(format_str, line)
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

        return num_req, dict_common, dict_freq, dict_4xx, dict_5xx
