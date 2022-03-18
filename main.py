"""Модуль, который описывает класс Money"""

from typing import Optional

from cache import cache, valutes, URL
from errors import ValuteTypeError
from utils import check_types, check_type


class Money:
    """Класс, который описывает денежные средства.

    Валюта выбирается пользователем из числа валют, представленных на сайте ЦБ РФ (см. valute.json),
    или рубли (RUR).
    Денежные средства могут быть конвертированы по текущему курсу ЦБ РФ. Для конвертации рублей в доллары
    предусмотрен отдельный метод convert_to_usd().

    Методы класса:
    convert_to_usd(): конвертирует рубли в доллары США по текущему курсу или последнему сохраненному курсу
    при отсутствии возможности получить данные с сайта ЦБ РФ при запуске скрипта.
    convert_to_valute(): конвертирует любую валюту в любую другую валюту по текущему курсу или
    последнему сохраненному курсу при отсутствии возможности получить данные с сайта ЦБ РФ
    при запуске скрипта."""

    def __init__(self, value: int | float, name: Optional[str] = None):
        """Инициализируем экземпляр класса Money

        :param value: количество денег
        :param name: наименование валюты. Наименование указывается в виде латинского буквенного кода (см. valute.json)
        или 'RUR' для рублей.
        """

        check_type(value, (int | float))
        self.value = value
        self.name = name

        if name != 'RUR' and name not in valutes().keys():
            raise ValuteTypeError

    def __add__(self, other: 'Money'):
        check_type(other, Money)
        if self.name == other.name:
            return Money(self.value + other.value, self.name)
        raise ValuteTypeError

    def __sub__(self, other: 'Money'):
        check_type(other, Money)
        if self.name == other.name:
            return Money(self.value - other.value, self.name)
        raise ValuteTypeError

    def __mul__(self, other: int | float):
        check_types(other, (int, float))
        return Money(self.value * other, self.name)

    def __truediv__(self, other: int | float):
        check_types(other, (int, float))
        return Money(self.value / other, self.name)

    def __eq__(self, other: 'Money'):
        check_type(other, Money)
        return self.value == other.value

    def __ne__(self, other: 'Money'):
        check_type(other, Money)
        return self.value != other.value

    def __lt__(self, other: 'Money'):
        check_type(other, Money)
        return self.value < other.value

    def __le__(self, other: 'Money'):
        check_type(other, Money)
        return self.value <= other.value

    def __gt__(self, other: 'Money'):
        check_type(other, Money)
        return self.value > other.value

    def __ge__(self, other: 'Money'):
        check_type(other, Money)
        return self.value >= other.value

    @classmethod
    def _convert_to_usd(cls, obj: 'Money', valute='USD'):
        """Метод класса, который конвертируем рубли в доллары США по текущему курсу ЦБ РФ
        или по последнему сохраненному курсу при отсутствии интернета (см. file.json)

        """

        check_type(obj, (Money))
        t = cache(URL)['Valute']['USD']['Value']
        return cls(obj.value / t, valute)

    @classmethod
    def _convert_to_valute(cls, obj: 'Money', valute: str):
        """Метод класса, который конвертирует рубли, а также любую валюту из списка valute.json в
        другую валюту из списка valute.json по текущему курсу ЦБ РФ или по последнему сохраненному курсу
        при отсутствии интернета (см. file.json)

        """

        check_type(obj, (Money))
        if valute != 'RUR' and valute not in valutes().keys():
            raise ValuteTypeError
        # конвертируем рубли
        if obj.name == 'RUR':
            t = cache(URL)['Valute'][valute]['Value']
            n = cache(URL)['Valute'][valute]['Nominal']
            return cls(obj.value / (t / n), valute)
        # конвертируем валюту, отличную от рублей
        else:
            # конвертируем в рубли
            t_rur = cache(URL)['Valute'][obj.name]['Value']
            n_rur = cache(URL)['Valute'][obj.name]['Nominal']
            rur = cls(obj.value / n_rur * t_rur, 'RUR')
            if valute == 'RUR':
                return rur
            # конвертируем в валюту, отличную от рублей
            else:
                t = cache(URL)['Valute'][valute]['Value']
                n = cache(URL)['Valute'][valute]['Nominal']
                return cls(rur.value / (t / n), valute)

    def __str__(self):
        return f'{self.value.__round__(2)} {self.name}'


if __name__ == '__main__':
    rur_1 = Money(8.73917, 'RUR')
    rur_2 = Money(5.5286, 'RUR')
    rur_3 = Money(100, 'RUR')
    rur_4 = Money(100, 'USD')
    print(rur_1, rur_2, rur_3)

    print(rur_1 + rur_2)
    print(rur_1 - rur_2)
    rur_1 *= 2
    print(rur_1)
    print(rur_2 / 2)
    print(rur_4 >= rur_3)
    print(rur_2 == rur_3)

    print(rur_1, Money._convert_to_usd(rur_1))
    print(rur_3, Money._convert_to_valute(rur_3, 'AMD'))
    print(rur_4, Money._convert_to_valute(rur_4, 'EUR'))
    print(rur_4, Money._convert_to_valute(rur_4, 'RUR'))
