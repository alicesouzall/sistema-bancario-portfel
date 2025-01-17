from typing import Any
import psycopg as pg
from psycopg.rows import DictRow
from domain.errors import DatabaseErrorHandler
from domain.ports import DatabaseConnectionInterface
# from infra.adapter.database import DatabaseFactory

class DatabaseConnection(DatabaseConnectionInterface):
    connection: pg.Connection
    cursor: pg.Cursor

    def __init__(self, connection: pg.Connection, cursor: pg.Cursor):
        self.connection = connection
        self.cursor = cursor

    def commit(self) -> None:
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self) -> None:
        self.connection.close()

    def execute_query(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] = ()
    ) -> list[DictRow] | DictRow | None:
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            if (
                isinstance(e, pg.ProgrammingError) and
                e.args[0] == "the last operation didn't produce a result"
            ):
                return []
            else:
                self.rollback()
                DatabaseErrorHandler().handle_pg_exceptions(e)
