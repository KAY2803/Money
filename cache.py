import json
import requests


FILE = 'file.json'
VAL = 'valute.json'
URL = 'https://www.cbr-xml-daily.ru/daily_json.js'


def full_cache(URL):
    try:
        if requests.get(URL):
            data = requests.get(URL).json()
            with open(FILE, 'w', encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
    except requests.exceptions.ConnectionError:
        print('Отсутствует соединение')


def from_cache():
    with open(FILE) as f:
        data = json.load(f)
        return data


def valutes():
    try:
        val = requests.get(URL).json()['Valute']
        with open(VAL, 'w', encoding="utf-8") as f:
            json.dump(val, f, indent=4, ensure_ascii=False)
            return val
    except requests.exceptions.ConnectionError:
        with open(VAL, encoding="utf-8") as f:
            val = json.load(f)
            return val


if __name__ == '__main__':
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    print(full_cache(url))
    # print(from_cache())
    print(valutes())