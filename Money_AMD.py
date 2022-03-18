from cache import cache, url
from main import Money


class AMD(Money):

    def convert_to_rur(self):
        t = cache(url)['Valute']['AMD']['Value']
        n = cache(url)['Valute']['AMD']['Nominal']
        return Money(round(self.value / n * t, 2), 'RUR')


if __name__ == '__main__':
    amd_1 = AMD(55, 'AMD')
    rur_1 = amd_1.convert_to_rur()
    print(amd_1, rur_1)