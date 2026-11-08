"""Тесты пакета poloshkov-mtp-utils, написанные до реализации."""

from __future__ import annotations

import pytest

from poloshkov_mtp_utils import (
    __version__,
    character_count,
    extract_words,
    top_words,
    word_count,
)


def test_extract_words_ignores_punctuation_and_case() -> None:
    """Слова извлекаются без знаков препинания и в нижнем регистре."""
    text = "Python, PYTHON! python; pytest."
    assert extract_words(text) == ["python", "python", "python", "pytest"]


def test_extract_words_supports_cyrillic_and_hyphen() -> None:
    """Unicode и дефис внутри слова обрабатываются корректно."""
    assert extract_words("Клиент-сервер, МОСКВА") == [
        "клиент-сервер",
        "москва",
    ]


def test_word_count() -> None:
    """Подсчёт учитывает слова, а не пробелы между ними."""
    assert word_count("  Один, два!\nТри.  ") == 3
    assert word_count("") == 0
    assert word_count(" , ! \n") == 0


def test_top_words_orders_by_frequency_then_alphabet() -> None:
    """Частоты убывают, а равные частоты сортируются по алфавиту."""
    assert top_words("b a b a c", limit=2) == [("a", 2), ("b", 2)]


def test_top_words_limit() -> None:
    """Ограничение отсекает менее частые слова."""
    assert top_words("a a a b b c", limit=2) == [("a", 3), ("b", 2)]


@pytest.mark.parametrize("limit", [0, -1, -100])
def test_top_words_rejects_non_positive_limit(limit: int) -> None:
    """Нулевой и отрицательный limit запрещены."""
    with pytest.raises(ValueError, match="положительным"):
        top_words("текст", limit=limit)


def test_character_count() -> None:
    """Можно считать все символы или только непробельные."""
    text = "a b\n"
    assert character_count(text) == 4
    assert character_count(text, ignore_spaces=True) == 2


def test_version_is_available() -> None:
    """Версия пакета доступна пользователю после импорта."""
    assert __version__ == "1.0.0"
