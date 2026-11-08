# poloshkov-mtp-utils

Учебный пакет для базовой статистики текста: извлечение слов, подсчёт
количества слов и символов, список самых частых слов. Не имеет внешних
зависимостей, поддерживает Python 3.10+ и Unicode.

## Установка с TestPyPI

После публикации релиза 1.0.0:

```bash
python -m pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  poloshkov-mtp-utils==1.0.0
```

Дополнительный индекс нужен только для возможных зависимостей сборки;
сам пакет зависит исключительно от стандартной библиотеки.

## Пример

```python
from poloshkov_mtp_utils import top_words, word_count

text = "Python, Python и pytest"
print(word_count(text))  # 4
print(top_words(text))   # [('python', 2), ('pytest', 1), ('и', 1)]
```

Порядок слов с одинаковой частотой алфавитный, поэтому результат всегда
воспроизводим.

## Разработка

```bash
python -m pytest -v
python -m build
python -m twine check dist/*
python -m twine upload --repository testpypi dist/*
```

Для последней команды используется API-токен TestPyPI: имя пользователя
`__token__`, пароль — значение токена. Токен не хранится в репозитории.
