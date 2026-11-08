"""TDD-тесты калькулятора: написаны до его реализации."""

from __future__ import annotations

import pytest

from task04_calculator import Calculator


@pytest.fixture()
def calculator() -> Calculator:
    """Возвращает независимый экземпляр калькулятора."""
    return Calculator()


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [(2, 3, 5), (-2, 3, 1), (0, 0, 0), (0.1, 0.2, 0.3)],
)
def test_add(calculator: Calculator, left: float, right: float,
             expected: float) -> None:
    """Сложение работает с положительными, отрицательными и float."""
    assert calculator.add(left, right) == pytest.approx(expected)


def test_subtract(calculator: Calculator) -> None:
    """Вычитание сохраняет порядок операндов."""
    assert calculator.subtract(10, 4) == 6
    assert calculator.subtract(4, 10) == -6


def test_multiply(calculator: Calculator) -> None:
    """Умножение поддерживает отрицательные числа и ноль."""
    assert calculator.multiply(6, 7) == 42
    assert calculator.multiply(-3, 5) == -15
    assert calculator.multiply(100, 0) == 0


def test_divide(calculator: Calculator) -> None:
    """Деление возвращает обычный числовой результат."""
    assert calculator.divide(9, 2) == 4.5
    assert calculator.divide(-8, 2) == -4


@pytest.mark.parametrize("divisor", [0, 0.0, -0.0])
def test_divide_by_zero(calculator: Calculator, divisor: float) -> None:
    """Любое представление нуля вызывает понятную ошибку."""
    with pytest.raises(ValueError, match="деление на ноль"):
        calculator.divide(1, divisor)
