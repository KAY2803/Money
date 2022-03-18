from typing import Optional

from cache import cache, valutes, url
from errors import ValuteTypeError
from utils import check_types, check_type


class Money:

    def __init__(self, value: int | float, name: Optional[str] = None):
        check_type(value, (int | float))
        self.value = value
        self.name = name

    def __add__(self, other):
        check_type(other, Money)
        if self.name == other.name:
            return Money(round(self.value + other.value, 2), self.name)
        raise ValuteTypeError

    def __sub__(self, other):
        check_type(other, Money)
        if self.name == other.name:
            return Money(round(self.value - other.value, 2), self.name)
        raise ValuteTypeError

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

    # def round(self, ndigits=None):
    #      return round(self._val, ndigits=ndigits)

    @classmethod
    def convert_to_usd(cls, obj: 'Money', valute='USD'):
        check_type(obj, (Money))
        t = cache(url)['Valute']['USD']['Value']
        return cls(round(obj.value / t, 2), valute)

    @classmethod
    def convert_to_valute(cls, obj: 'Money', valute: str):
        check_type(obj, (Money))
        if valute not in valutes().keys():
            raise ValuteTypeError
        t = cache(url)['Valute'][valute]['Value']
        n = cache(url)['Valute'][valute]['Nominal']
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
