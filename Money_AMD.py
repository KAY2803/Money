from main import Money
from cache import full_cache, from_cache, URL
import requests


class AMD(Money):

    def convert_to_rur(self):
        try:
            if requests.get(URL).status_code == 200:
                full_cache(URL)
                t = requests.get(URL).json()['Valute']['AMD']['Value']
                n = requests.get(URL).json()['Valute']['AMD']['Nominal']
                return Money(round(self.value / n * t, 2), 'RUR')
        except requests.exceptions.ConnectionError:
            t = from_cache()['Valute']['AMD']['Value']
            n = from_cache()['Valute']['AMD']['Nominal']
            return Money(round(self.value / n * t, 2), 'RUR')


if __name__ == '__main__':
    amd_1 = AMD(55, 'AMD')
    rur_1 = amd_1.convert_to_rur()
    print(amd_1, rur_1)