"""Задание 4 (средняя сложность): калькулятор, разработанный через TDD.

Сначала были написаны тесты в tests/test_task04_calculator.py, затем
реализация класса Calculator. Порядок виден в истории коммитов.

Запуск демонстрации: python task04_calculator.py
"""

from __future__ import annotations

Number = int | float


class Calculator:
    """Калькулятор четырёх арифметических операций."""

    @staticmethod
    def add(left: Number, right: Number) -> Number:
        """Возвращает сумму двух чисел."""
        return left + right

    @staticmethod
    def subtract(left: Number, right: Number) -> Number:
        """Возвращает разность двух чисел."""
        return left - right

    @staticmethod
    def multiply(left: Number, right: Number) -> Number:
        """Возвращает произведение двух чисел."""
        return left * right

    @staticmethod
    def divide(left: Number, right: Number) -> Number:
        """Делит left на right; запрещает деление на ноль."""
        if right == 0:
            raise ValueError("деление на ноль запрещено")
        return left / right


def demo() -> None:
    """Показывает результаты всех операций и обработку ошибки."""
    calculator = Calculator()
    print("2 + 3 =", calculator.add(2, 3))
    print("10 - 4 =", calculator.subtract(10, 4))
    print("6 * 7 =", calculator.multiply(6, 7))
    print("9 / 2 =", calculator.divide(9, 2))
    try:
        calculator.divide(1, 0)
    except ValueError as error:
        print("1 / 0 ->", error)


if __name__ == "__main__":
    demo()
