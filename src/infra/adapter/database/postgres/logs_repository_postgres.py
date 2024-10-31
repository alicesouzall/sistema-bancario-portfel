from dataclasses import asdict
import json
from domain.models import Logs
from domain.ports import LogsRepositoryInterface
from infra.adapter.database import DatabaseConnection


class LogsRepositoryPostgres(LogsRepositoryInterface):
    connection: DatabaseConnection

    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def create(self, log: Logs) -> None:
        query = """
            INSERT INTO logs (
                id,
                error,
                context,
                message,
                date
            ) VALUES (
                %(id)s, %(error)s, %(context)s,
                %(message)s, %(date)s
            )
        """
        self.connection.execute_query(query, {
            **asdict(log), "context": json.dumps(asdict(log.context))
        })
