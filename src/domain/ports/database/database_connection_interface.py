from typing import Any

class DatabaseConnectionInterface():
    def commit(self) -> None:
        raise NotImplementedError("DatabaseConnection")

    def rollback(self):
        raise NotImplementedError("DatabaseConnection")

    def close(self) -> None:
        raise NotImplementedError("DatabaseConnection")

    def execute_query(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] = ()
    ) -> list[tuple] | None:
        raise NotImplementedError("DatabaseConnection")
