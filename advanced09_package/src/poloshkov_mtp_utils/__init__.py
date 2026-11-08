"""Небольшой пакет для подсчёта статистики по тексту."""

from .textstats import character_count, extract_words, top_words, word_count

__version__ = "1.0.0"

__all__ = [
    "character_count",
    "extract_words",
    "top_words",
    "word_count",
    "__version__",
]
