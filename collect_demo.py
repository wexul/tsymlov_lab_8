"""Собирает demo_output.txt реальными проверками репозитория."""

from __future__ import annotations

import datetime
import platform
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEPARATOR = "-" * 70
output: list[str] = []
failures: list[str] = []


def run(title: str, command: list[str]) -> None:
    """Выполняет команду и сохраняет вывод вместе с кодом возврата."""
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    output.extend([SEPARATOR, title, SEPARATOR, "$ " + " ".join(command), ""])
    if result.stdout.strip():
        output.append(result.stdout.rstrip("\n"))
    if result.stderr.strip():
        output.append(result.stderr.rstrip("\n"))
    output.extend(["", f"код возврата: {result.returncode}", ""])
    if result.returncode != 0:
        failures.append(title)


def main() -> None:
    """Запускает демонстрации, тесты, flake8 и сборку пакета."""
    output.extend([
        "Лабораторная работа №8, вариант 4 - фактические запуски",
        "=" * 70,
        "",
        "Дата выполнения: " + datetime.date.today().strftime("%d.%m.%Y"),
        "Python: " + platform.python_version(),
        "ОС: " + platform.platform(),
        "",
        "Каждый раздел содержит команду, фактический вывод и код возврата.",
        "",
    ])

    run("Задание 4 (средняя). Калькулятор",
        ["py", "-3", "task04_calculator.py"])

    api_code = (
        "from fastapi.testclient import TestClient; "
        "from advanced05_books_api import create_app; "
        "client = TestClient(create_app()); "
        "response = client.post('/books', json={'title': 'Чистый код', "
        "'author': 'Роберт Мартин', 'year': 2008}); "
        "print('POST /books:', response.status_code, response.json()); "
        "book_id = response.json()['id']; "
        "print('GET /books:', client.get('/books').status_code, "
        "client.get('/books').json()); "
        "print('DELETE /books:', "
        "client.delete(f'/books/{book_id}').status_code); "
        "print('GET удалённой:', "
        "client.get(f'/books/{book_id}').status_code); "
        "client.close()"
    )
    run("Задание 5 (повышенная). FastAPI CRUD",
        ["py", "-3", "-c", api_code])

    package_code = (
        "import sys; sys.path.insert(0, 'advanced09_package/src'); "
        "from poloshkov_mtp_utils import top_words, word_count; "
        "text = 'Python, Python и pytest'; "
        "print('word_count:', word_count(text)); "
        "print('top_words:', top_words(text))"
    )
    run("Задание 9 (повышенная). Демонстрация своего пакета",
        ["py", "-3", "-c", package_code])

    run("Все pytest-тесты: калькулятор, API и пакет",
        ["py", "-3", "-m", "pytest", "-v"])
    run("Задание 6 (средняя). Проверка стиля flake8",
        ["py", "-3", "-m", "flake8", "."])
    run("Задание 9 (повышенная). Сборка wheel и sdist",
        ["py", "-3", "-m", "build", "advanced09_package"])

    dist = ROOT / "advanced09_package" / "dist"
    distributions = [
        str(path.relative_to(ROOT))
        for path in sorted(dist.iterdir())
        if path.suffix in {".whl", ".gz"}
    ]
    if distributions:
        run("Проверка метаданных дистрибутивов twine",
            ["py", "-3", "-m", "twine", "check", *distributions])
    else:
        failures.append("дистрибутивы не найдены")

    publication_code = (
        "import json, urllib.request; "
        "url = 'https://test.pypi.org/pypi/poloshkov-mtp-utils/1.0.0/json'; "
        "data = json.load(urllib.request.urlopen(url)); "
        "assert data['info']['version'] == '1.0.0'; "
        "assert len(data['urls']) == 2; "
        "print('TestPyPI version:', data['info']['version']); "
        "print('Published files:', len(data['urls'])); "
        "print('Project URL:', data['info']['project_url'])"
    )
    run("Проверка публикации пакета на TestPyPI",
        ["py", "-3", "-c", publication_code])

    (ROOT / "demo_output.txt").write_text(
        "\n".join(output).rstrip("\n") + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("demo_output.txt записан, строк:", len(output))
    if failures:
        raise SystemExit("Ошибки: " + "; ".join(failures))


if __name__ == "__main__":
    main()
