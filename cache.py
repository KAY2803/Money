import json
import requests


FILE = 'file.json'
VAL = 'valute.json'
url = 'https://www.cbr-xml-daily.ru/daily_json.js'


def cache(url):
    try:
        if requests.get(url).status_code == 200:
            data = requests.get(url).json()
            with open(FILE, 'w', encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                return data
    except requests.exceptions.ConnectionError:
        with open(FILE, encoding="utf-8") as f:
            data = json.load(f)
            return data


def valutes():
    try:
        val = requests.get(url).json()['Valute']
        with open(VAL, 'w', encoding="utf-8") as f:
            json.dump(val, f, indent=4, ensure_ascii=False)
            return val
    except requests.exceptions.ConnectionError:
        with open(VAL, encoding="utf-8") as f:
            val = json.load(f)
            return val


if __name__ == '__main__':
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    print(cache(url))
    print(valutes())
