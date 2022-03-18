"""Модуль, который описывает создание и обновление данных о курсах валют"""

from datetime import date
import json
import requests



FILE = 'file.json'
VAL = 'valute.json'
URL = 'https://www.cbr-xml-daily.ru/daily_json.js'
DATE = {'Последняя дата обновления ': str(date.today())}


def cache(URL):
    """Функция, которая получает и сохраняет в file.json данные о текущих курсах валют с сайта ЦБ РФ"""
    try:
        if requests.get(URL).status_code == 200:
            data = requests.get(URL).json()
            data.update(DATE)
            with open(FILE, 'w', encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                return data
    # при отсутствии интернета данные берутся из file.json
    except requests.exceptions.ConnectionError:
        with open(FILE, encoding="utf-8") as f:
            data = json.load(f)
            return data


def valutes():
    """Функция, которая получает и сохраняет в valute.json данные о текущих валютах с сайта ЦБ РФ"""
    try:
        val = requests.get(URL).json()['Valute']
        with open(VAL, 'w', encoding="utf-8") as f:
            json.dump(val, f, indent=4, ensure_ascii=False)
            return val
    # при отсутствии интернета данные берутся из valute.json
    except requests.exceptions.ConnectionError:
        with open(VAL, encoding="utf-8") as f:
            val = json.load(f)
            return val


if __name__ == '__main__':
    URL = 'https://www.cbr-xml-daily.ru/daily_json.js'
    print(cache(URL))
    # print(valutes().keys())
    # print(DATE)
