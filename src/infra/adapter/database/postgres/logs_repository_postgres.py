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
                status_code,
                context,
                message,
                date,
                account_id
            ) VALUES (
                %(id)s, %(status_code)s, %(context)s,
                %(message)s, %(date)s, %(account_id)s
            )
        """
        self.connection.execute_query(query, {
            **asdict(log), "context": json.dumps(log.context)
        })

    def get_statement_by_account_id(self, account_id: str) -> list[Logs] | None:
        query = """
            SELECT * FROM logs WHERE account_id = %s
            AND status_code = 200
        """
        logs = self.connection.execute_query(query, (account_id,))
        return [
            Logs(**l) for l in logs
        ]
