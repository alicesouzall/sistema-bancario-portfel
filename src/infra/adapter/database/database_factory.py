from contextlib import contextmanager
from typing import Any, Generator
import psycopg as pg
from psycopg.rows import dict_row
import os
from domain.errors import DatabaseErrorHandler
from infra.adapter.database.database_connection import DatabaseConnection

class DatabaseFactory():
    host: str | None
    name: str | None
    username: str | None
    password: str | None
    port: str | None

    def __init__(self) -> tuple[pg.Connection, pg.Cursor]:
        self.host = os.getenv("DATABASE_HOST")
        self.name = os.getenv("DATABASE_NAME")
        self.username = os.getenv("DATABASE_USERNAME")
        self.password = os.getenv("DATABASE_PASSWORD")
        self.port = os.getenv("DATABASE_PORT")

    @contextmanager
    def create_postgres_connection(self):
        connection = pg.connect(
            host=self.host,
            dbname=self.name,
            user=self.username,
            password=self.password,
            port=self.port,
        )
        cursor = connection.cursor(row_factory=dict_row)
        connection.autocommit = False

        try:
            yield DatabaseConnection(connection, cursor)
        except Exception as e:
            DatabaseErrorHandler().handle_pg_connection_exceptions(e)
        finally:
            cursor.close()
            connection.close()
