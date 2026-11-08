"""Функции анализа текста без внешних зависимостей."""

from __future__ import annotations

import re
from collections import Counter

WORD_PATTERN = re.compile(r"\w+(?:[-']\w+)*", flags=re.UNICODE)


def extract_words(text: str) -> list[str]:
    """Извлекает слова, игнорирует пунктуацию и приводит к нижнему регистру."""
    return [match.group().casefold() for match in WORD_PATTERN.finditer(text)]


def word_count(text: str) -> int:
    """Возвращает количество слов в тексте."""
    return len(extract_words(text))


def top_words(text: str, limit: int = 5) -> list[tuple[str, int]]:
    """Возвращает самые частые слова и их количество.

    При одинаковой частоте порядок алфавитный, поэтому результат
    детерминирован и удобен для отображения и тестирования.
    """
    if limit <= 0:
        raise ValueError("limit должен быть положительным")
    counts = Counter(extract_words(text))
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ordered[:limit]


def character_count(text: str, ignore_spaces: bool = False) -> int:
    """Считает символы; при ignore_spaces исключает все пробельные."""
    if ignore_spaces:
        return sum(not character.isspace() for character in text)
    return len(text)
