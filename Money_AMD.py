"""Модуль, который описывает класс AMD - дочерний класс класса Money"""

from cache import cache, URL
from main import Money


class AMD(Money):
    """Класс, который описывает армянскую валюту - армянские драмы (AMD)"""

    def _convert_to_rur(self):
        """Метод экземпляра, который позволяет конвертировать армянские драмы в рубли по текущему курсу ЦБ РФ
        или по последнему сохраненному курсу при отсутствии интернета (см. file.json)

        """

        t = cache(URL)['Valute']['AMD']['Value']
        n = cache(URL)['Valute']['AMD']['Nominal']
        return Money(self.value / n * t, 'RUR')


if __name__ == '__main__':
    amd_1 = AMD(55, 'AMD')
    rur_1 = amd_1._convert_to_rur()
    print(amd_1, rur_1)