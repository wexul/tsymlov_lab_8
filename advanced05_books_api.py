"""Задание 5 (повышенная сложность): TDD для REST API.

API книг реализовано после написания tests/test_advanced05_api.py.
Фабрика create_app создаёт независимое хранилище для каждого приложения,
поэтому тесты не влияют друг на друга.

Запуск сервера: uvicorn advanced05_books_api:app --reload
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field


class BookInput(BaseModel):
    """Данные книги, принимаемые от клиента."""

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=200)
    year: int = Field(ge=0, le=2100)


class Book(BookInput):
    """Книга с назначенным сервером идентификатором."""

    id: int


def create_app() -> FastAPI:
    """Создаёт приложение FastAPI с изолированным хранилищем книг."""
    application = FastAPI(
        title="Библиотека — TDD API",
        version="1.0.0",
        description="CRUD API, разработанный по циклу red-green-refactor.",
    )
    books: dict[int, Book] = {}
    next_id = 1

    @application.post(
        "/books", response_model=Book, status_code=status.HTTP_201_CREATED
    )
    def create_book(payload: BookInput) -> Book:
        """Создаёт книгу и возвращает её с идентификатором."""
        nonlocal next_id
        book = Book(id=next_id, **payload.model_dump())
        books[next_id] = book
        next_id += 1
        return book

    @application.get("/books", response_model=list[Book])
    def list_books(author: str | None = None) -> list[Book]:
        """Возвращает книги, при необходимости фильтруя по автору."""
        result = list(books.values())
        if author is not None:
            result = [
                book for book in result
                if author.casefold() in book.author.casefold()
            ]
        return result

    @application.get("/books/{book_id}", response_model=Book)
    def get_book(book_id: int) -> Book:
        """Возвращает книгу по id либо ошибку 404."""
        if book_id not in books:
            raise HTTPException(status_code=404, detail="Книга не найдена")
        return books[book_id]

    @application.put("/books/{book_id}", response_model=Book)
    def update_book(book_id: int, payload: BookInput) -> Book:
        """Полностью обновляет существующую книгу."""
        if book_id not in books:
            raise HTTPException(status_code=404, detail="Книга не найдена")
        book = Book(id=book_id, **payload.model_dump())
        books[book_id] = book
        return book

    @application.delete(
        "/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT
    )
    def delete_book(book_id: int) -> None:
        """Удаляет книгу; отсутствующий id даёт ошибку 404."""
        if book_id not in books:
            raise HTTPException(status_code=404, detail="Книга не найдена")
        del books[book_id]

    return application


app = create_app()
