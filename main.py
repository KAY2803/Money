import json

import requests
from errors import *

from cache import full_cache, from_cache, valutes, URL
from typing import Optional
from utils import check_types, check_type


class Money:

    def __init__(self, value: int | float, name: Optional[str] = None):
        check_type(value, (int | float))
        self.value = value
        self.name = name

    def __add__(self, other):
        check_type(other, Money)
        return Money(round(self.value + other.value, 2), self.name)

    def __sub__(self, other):
        check_type(other, Money)
        return Money(round(self.value - other.value, 2), self.name)

    def __mul__(self, other: int | float):
        check_types(other, (int, float))
        return Money(round(self.value * other, 2), self.name)

    def __truediv__(self, other: int | float):
        check_types(other, (int, float))
        return Money(round(self.value / other, 2), self.name)

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
    def convert_to_usd(cls, obj: 'Money', valute='USD'):
        check_type(obj, (Money))
        try:
            if requests.get(URL).status_code == 200:
                full_cache(URL)
                t = requests.get(URL).json()['Valute']['USD']['Value']
                return cls(round(obj.value / t, 2), valute)
        except requests.exceptions.ConnectionError:
            t = from_cache()['Valute']['USD']['Value']
            return cls(round(obj.value / t, 2), valute)

    @classmethod
    def convert_to_valute(cls, obj: 'Money', valute: str):
        check_type(obj, (Money))
        if not valute in valutes().keys():
            raise ValuteTypeError
        try:
            if requests.get(URL).status_code == 200:
                full_cache(URL)
                t = requests.get(URL).json()['Valute'][valute]['Value']
                n = requests.get(URL).json()['Valute'][valute]['Nominal']
                return cls(round(obj.value / (t / n), 2), valute)
        except requests.exceptions.ConnectionError:
            t = from_cache()['Valute'][valute]['Value']
            n = from_cache()['Valute'][valute]['Nominal']
            return cls(round(obj.value / (t / n), 2), valute)

    def __str__(self):
        return f'{self.value} {self.name}'


if __name__ == '__main__':
    rur_1 = Money(8.73, 'RUR')
    rur_2 = Money(5.52, 'RUR')
    rur_3 = Money(100, 'RUR')
    print(rur_1, rur_2, rur_3)

    print(rur_1 + rur_2)
    print(rur_1 - rur_2)
    rur_1 *= 2
    print(rur_1)
    print(rur_2 / 2)
    print(rur_2 >= rur_1)
    print(rur_2 < rur_3)

    print(rur_1, Money.convert_to_usd(rur_1))
    print(rur_3, Money.convert_to_valute(rur_3, 'AMD'))
