"""Модуль, который содержит функции для проверки типов данных check_type и check_types"""

from typing import Any


def check_type(value: Any, types: Any):
    """Функция, которая проверяет тип введеного значения на соовтетствие одному типу"""
    if not isinstance(value, types):
        raise TypeError(f"Ожидается {types}, получено {type(value)}")
    else:
        return value


def check_types(values: Any, types_: tuple):
    """Функция, которая проверяет типы введеного значения/ значений на соовтетствие двум и более типам"""

    if not isinstance(values, tuple):
        values = (values,)

    for elem in values:
        check_type(elem, types_)


if __name__ == '__main__':
    a = 10
    b = 10
    tup = (a, b)
    check_type(tup, tuple)


