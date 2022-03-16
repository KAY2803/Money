import json
import requests
from typing import Union, Optional
from utils import check_types, check_type


class Money:

    def __init__(self, name: str, value: float):
        self.name = name
        self.value = value

    def __add__(self, other):
        check_type(other, Money)
        if self.name == other.name:
            return Money(self.name, round(self.value + other.value, 2))

    # добавить else (конвертация в одну валюту) или ошибку

    def __sub__(self, other):
        check_type(other, Money)
        if self.name == other.name:
            return Money(self.name, round(self.value - other.value, 2))

    # добавить else (конвертация в одну валюту) или ошибку

    def __mul__(self, other: int | float):
        check_types(other, (int, float))
        return Money(self.name, round(self.value * other, 2))

    def __truediv__(self, other: int | float):
        check_types(other, (int, float))
        return Money(self.name, round(self.value / other, 2))

    def __eq__(self, other):
        check_type(other, Money)
        return self.value == other.value

    def __ne__(self, other):
        check_type(other, Money)
        return self.value != other.value

    def __lt__(self, other):
        check_type(other, Money)
        return self.value < other.value

    def __le__(self, other):
        check_type(other, Money)
        return self.value <= other.value

    def __gt__(self, other):
        check_type(other, Money)
        return self.value > other.value

    def __ge__(self, other):
        check_type(other, Money)
        return self.value >= other.value

    # добавить магический метод round
    # def round(self, ndigits=None):
    #     return round(self._val, ndigits=ndigits)

    @classmethod
    def convert_to_usd(cls, name: str, value: int | float):
        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        answer = requests.get(url=url)
        cache = answer.json()
        if answer:
            cache = answer.json()
            t = cache['Valute']['USD']['Value']
            return Money('USD', round(value * t, 2))
        else:
            t = cache['Valute']['USD']['Value']
            return Money('USD', round(value * t, 2))

    def __str__(self):
        return f'{self.value} {self.name}'


if __name__ == '__main__':
    rur_1 = Money('RUR', 8.73)
    rur_2 = Money('RUR', 5.52)
    rur_3 = Money('RUR', 5.52)

    print(Money.convert_to_usd('RUR', 10))
    # print(rur_1 + rur_2)
    # print(rur_1 - rur_2)
    # rur_1 *= 2
    # print(rur_1)
    # print(rur_2 / 2)
    # print(rur_2 >= rur_1)
    # print(rur_2 > rur_3)
