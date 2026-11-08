"""TDD-тесты API книг: контракт описан до реализации FastAPI."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from advanced05_books_api import create_app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    """Создаёт новый TestClient и пустое хранилище для каждого теста."""
    with TestClient(create_app()) as test_client:
        yield test_client


def add_book(client: TestClient, title: str = "Чистый код",
             author: str = "Роберт Мартин", year: int = 2008) -> dict:
    """Добавляет тестовую книгу и возвращает ответ сервера."""
    response = client.post(
        "/books",
        json={"title": title, "author": author, "year": year},
    )
    assert response.status_code == 201
    return response.json()


def test_create_book(client: TestClient) -> None:
    """POST создаёт ресурс и возвращает 201 и все его поля."""
    book = add_book(client)
    assert book == {
        "id": 1,
        "title": "Чистый код",
        "author": "Роберт Мартин",
        "year": 2008,
    }


def test_create_strips_outer_whitespace(client: TestClient) -> None:
    """Pydantic удаляет внешние пробелы из строковых полей."""
    book = add_book(client, title="  Рефакторинг  ")
    assert book["title"] == "Рефакторинг"


def test_list_books(client: TestClient) -> None:
    """GET возвращает все добавленные книги в порядке создания."""
    first = add_book(client)
    second = add_book(client, "Совершенный код", "Стив Макконнелл", 2004)
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == [first, second]


def test_filter_books_by_author_case_insensitive(
        client: TestClient) -> None:
    """Фильтр автора не зависит от регистра и ищет подстроку."""
    add_book(client)
    add_book(client, "Рефакторинг", "Мартин Фаулер", 1999)
    response = client.get("/books", params={"author": "мартин"})
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_existing_book(client: TestClient) -> None:
    """GET по id возвращает именно запрошенную книгу."""
    expected = add_book(client)
    response = client.get(f"/books/{expected['id']}")
    assert response.status_code == 200
    assert response.json() == expected


def test_get_missing_book_returns_404(client: TestClient) -> None:
    """Запрос отсутствующей книги возвращает понятную ошибку 404."""
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Книга не найдена"}


def test_update_book(client: TestClient) -> None:
    """PUT заменяет поля книги, сохраняя её идентификатор."""
    book = add_book(client)
    response = client.put(
        f"/books/{book['id']}",
        json={"title": "Чистый код", "author": "Роберт Мартин",
              "year": 2019},
    )
    assert response.status_code == 200
    assert response.json()["year"] == 2019
    assert response.json()["id"] == book["id"]


def test_update_missing_book_returns_404(client: TestClient) -> None:
    """Нельзя обновить несуществующий ресурс."""
    response = client.put(
        "/books/999",
        json={"title": "Книга", "author": "Автор", "year": 2020},
    )
    assert response.status_code == 404


def test_delete_book(client: TestClient) -> None:
    """DELETE возвращает 204, после чего книга недоступна."""
    book = add_book(client)
    response = client.delete(f"/books/{book['id']}")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/books/{book['id']}").status_code == 404


def test_delete_missing_book_returns_404(client: TestClient) -> None:
    """Повторное удаление несуществующего id возвращает 404."""
    assert client.delete("/books/999").status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"title": "", "author": "Автор", "year": 2020},
        {"title": "   ", "author": "Автор", "year": 2020},
        {"title": "Книга", "author": "", "year": 2020},
        {"title": "Книга", "author": "Автор", "year": -1},
        {"title": "Книга", "author": "Автор", "year": 2200},
    ],
)
def test_invalid_book_returns_422(client: TestClient,
                                  payload: dict) -> None:
    """Некорректные поля отклоняются схемой с ответом 422."""
    response = client.post("/books", json=payload)
    assert response.status_code == 422


def test_storage_is_isolated_between_clients() -> None:
    """Два приложения не разделяют изменяемое глобальное состояние."""
    with TestClient(create_app()) as first:
        add_book(first)
    with TestClient(create_app()) as second:
        assert second.get("/books").json() == []
