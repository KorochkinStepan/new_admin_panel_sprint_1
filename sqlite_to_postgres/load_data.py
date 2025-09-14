import logging
import os
import sqlite3

import psycopg
from dotenv import load_dotenv
from psycopg import ClientCursor, connection as _connection
from psycopg.rows import dict_row

from utils import load_data, get_logger


def load_from_sqlite(
    connection: sqlite3.Connection,
    pg_conn: _connection,
    tables: list[str],
    logger: logging.Logger,
):
    """Основной метод загрузки данных из SQLite в Postgres"""
    try:
        for table in tables:
            load_data(connection.cursor(), pg_conn.cursor(), table)
            logger.debug(f"Table {table} loaded")
    except Exception as e:
        logger.error(
            f"There is an error while loading data from {table} table : {str(e)}"
        )


if __name__ == "__main__":
    load_dotenv()
    BATCH_SIZE = os.environ.get("BATCH_SIZE", 100)

    dsl = {
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
        "host": os.environ.get("DB_HOST", "127.0.0.1"),
        "port": os.environ.get("DB_PORT", 5432),
    }
    logger = get_logger("SQLiteToPostgres")

    tables = ["film_work", "genre", "genre_film_work", "person", "person_film_work"]
    logger.debug(f"These tables will be saved to Postgres: {','.join(tables)}")

    with sqlite3.connect("db.sqlite") as sqlite_conn, psycopg.connect(
        **dsl, row_factory=dict_row, cursor_factory=ClientCursor
    ) as pg_conn:
        sqlite_conn.row_factory = sqlite3.Row
        load_from_sqlite(sqlite_conn, pg_conn, tables, logger)
