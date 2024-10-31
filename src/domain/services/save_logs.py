from datetime import datetime
from domain.enums import BankTransactionType
from domain.models import Logs, Context
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
        source_account: str,
        transaction_type: BankTransactionType | None = None,
        destination_account: str | None = None,
        current_balance: str | None = None,
        transaction_amount: str | None = None,
        error: bool = False
    ):
        try:
            if error:
                self.connection.rollback()

            context = Context(
                source_account=source_account,
                destination_account=destination_account,
                transaction_type=transaction_type,
                current_balance=current_balance,
                transaction_amount=transaction_amount
            )

            logs = Logs(
                id=self.uuid.generate_uuid(),
                error=error,
                context=context,
                message=message,
                date=datetime.now()
            )

            self.logs_repository.create(logs)

            self.connection.commit()

        except Exception as e:
            print(str(e))
