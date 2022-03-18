import random

from main import Money


class TestClassMoney:

    @classmethod
    def setUpClass(cls):
        cls.name = ['RUR', 'AMD', 'USD', 'EUR', 'GBP', 'AZN', 'BYN', 'BGN', 'BRL', 'HUF']
        moneys = []
        for i in range(10):
            cls.value = random.uniform(1, 1000000)
            moneys.append(dict(value=cls.value, name=cls.name[i]))
        return moneys

    def test_init(self):
        for i in range(10):
            a = self.setUpClass()[i]
            assert Money(a['value'], a['name']) == Money(a['value'], a['name']), 'Неверные параметры экземпляра'

    def test_add(self):
        for i in range(10):
            a = self.setUpClass()[i]
            assert Money(a['value'], a['name']) + Money(a['value'], a['name']) == Money(a['value'] * 2, a['name'])

    def test_mul(self):
        assert Money(4, 'RUR') * 4 == Money(16, 'RUR')

    def test_compare(self):
        assert Money(20, 'EUR') == Money(20, 'EUR')
        assert Money(987, 'RUR') != Money(9, 'RUR')
        assert Money(15, 'USD') < Money(20, 'USD')
        assert Money(15, 'EUR') > Money(20, 'RUR')
        assert Money(150, 'RUR') <= Money(200, 'RUR')
        assert Money(1000, 'USD') >= Money(20.98, 'RUR')

    def test_convert_to_usd(self):
        assert Money._convert_to_usd(Money(10000, 'RUR')) == Money(10000 / 103.9524, 'USD')

    def test_convert_to_valute(self):
        assert Money._convert_to_valute(Money(10000, 'USD'), 'EUR') == Money(10000 * 103.9524 / 114.3996, 'EUR')