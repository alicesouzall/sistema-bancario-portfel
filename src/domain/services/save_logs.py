from datetime import datetime
from domain.enums import BankTransactionType
from domain.models import Logs
from domain.ports import (
    LogsRepositoryInterface,
    DatabaseConnectionInterface,
    UuidInterface
)


class SaveLogs():
    def __init__(
        self,
        logs_repository: LogsRepositoryInterface,
        uuid: UuidInterface,
        connection: DatabaseConnectionInterface
    ):
        self.logs_repository = logs_repository
        self.connection = connection
        self.uuid = uuid

    def execute(
        self,
        message: str,
        account_id: str | None = None,
        context: dict[str, str] | None = None,
        status_code: int = 200.
    ):
        try:
            logs = Logs(
                id=self.uuid.generate_uuid(),
                status_code=status_code,
                context=context,
                message=message,
                date=datetime.now(),
                account_id=account_id
            )

            self.logs_repository.create(logs)

            self.connection.commit()

        except Exception as e:
            raise e
