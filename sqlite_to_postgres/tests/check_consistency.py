import os
import sqlite3

import psycopg
from psycopg import ClientCursor
from psycopg.rows import dict_row
from dotenv import load_dotenv
from sqlite_to_postgres.utils import test_transfer, get_logger

if __name__ == "__main__":
    load_dotenv()
    BATCH_SIZE = os.environ.get("BATCH_SIZE", 100)

    dsl = {
        "dbname": os.environ.get('DB_NAME'),
        "user": os.environ.get('DB_USER'),
        "password": os.environ.get('DB_PASSWORD'),
        "host": os.environ.get('DB_HOST', '127.0.0.1'),
        "port": os.environ.get('DB_PORT', 5432),
    }
    logger = get_logger("SQLiteToPostgres")

    tables = ["film_work","genre","genre_film_work","person","person_film_work"]

    with sqlite3.connect("../db.sqlite") as sqlite_conn, psycopg.connect(
            **dsl, row_factory= dict_row, cursor_factory=ClientCursor
    ) as pg_conn:
        sqlite_conn.row_factory = sqlite3.Row

        try:
            for table in tables:
                test_transfer(sqlite_conn.cursor(), pg_conn.cursor(), table)
                logger.info(f"Table: {table} checked successfully, all data is consistent")
            logger.info(f"Tables: {tables} checked successfully, all data is consistent")
        except Exception as e:
            logger.error(f"There is an error while checking data from {table} table : {str(e)}")
