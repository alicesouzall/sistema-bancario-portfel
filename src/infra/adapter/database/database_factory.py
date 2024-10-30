import psycopg as pg
from psycopg.rows import dict_row
import os
from domain.errors import DatabaseErrorHandler

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
        self.connection, self.cursor = self.create_postgres_connection()

    def create_postgres_connection(self) -> tuple[pg.Connection, pg.Cursor]:
        try:
            self.connection = pg.connect(
                host=self.host,
                dbname=self.name,
                user=self.username,
                password=self.password,
                port=self.port,
            )

            return self.connection, self.connection.cursor(row_factory=dict_row)
        except Exception as e:
            DatabaseErrorHandler(e)
