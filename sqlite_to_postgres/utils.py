import logging
import os
import sqlite3
import typing
from dataclasses import astuple, fields
from typing import Generator
from sqlite_to_postgres.classes import Genre, Person, FilmWork, GenreFilmWork, PersonFilmWork
import psycopg


table_to_class_mapping = {
    "film_work": FilmWork,
    "genre": Genre,
    "genre_film_work": GenreFilmWork,
    "person": Person,
    "person_film_work": PersonFilmWork,
}
BATCH_SIZE = os.environ.get("BATCH_SIZE", 100)


def extract_data(
    sqlite_cursor: sqlite3.Cursor, table_name: str
) -> Generator[list[sqlite3.Row], None, None]:
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    while results := sqlite_cursor.fetchmany(BATCH_SIZE):
        yield results


def transform_data(
    sqlite_cursor: sqlite3.Cursor, table_name: str
) -> Generator[list[typing.Union[Genre, Person, FilmWork]], None, None]:
    for batch in extract_data(sqlite_cursor, table_name=table_name):
        yield [table_to_class_mapping[table_name](**item) for item in batch]


def load_data(
    sqlite_cursor: sqlite3.Cursor, pg_cursor: psycopg.Cursor, table_name: str
):
    for batch in transform_data(sqlite_cursor, table_name=table_name):
        column_names = [field.name for field in fields(batch[0])]
        column_names_str = ",".join(column_names)
        placeholders = ",".join(["%s"] * len(column_names))

        query = f"INSERT INTO content.{table_name} ({column_names_str}) VALUES ({placeholders}) ON CONFLICT (id) DO NOTHING"
        batch_as_tuples = [astuple(item) for item in batch]
        pg_cursor.executemany(query, batch_as_tuples)


def test_transfer(
    sqlite_cursor: sqlite3.Cursor, pg_cursor: psycopg.Cursor, table_name: str
):
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")

    while batch := sqlite_cursor.fetchmany(BATCH_SIZE):
        original_batch = [
            table_to_class_mapping[table_name](**dict(item)) for item in batch
        ]
        ids = [student.id for student in original_batch]

        pg_cursor.execute(
            f"SELECT * FROM content.{table_name} WHERE id = ANY(%s)", [ids]
        )
        transferred_batch = [
            table_to_class_mapping[table_name](**item) for item in pg_cursor.fetchall()
        ]

        assert len(original_batch) == len(
            transferred_batch
        ), f"Не совпадает количество записей в таблице {table_name}"
        assert (
            original_batch == transferred_batch
        ), f"Не совпадают  записи в таблице {table_name}"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    return logger
