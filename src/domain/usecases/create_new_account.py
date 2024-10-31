import random
from decimal import Decimal
from domain.errors import UNKNOWN_ERROR
from domain.models import Account, Response
from domain.services import SaveLogs
from domain.ports import (
    UuidInterface,
    AccountRepositoryInterface,
    DatabaseConnectionInterface,
    LogsRepositoryInterface
)


class CreateNewAccount:
    def __init__(
        self,
        uuid: UuidInterface,
        account_repository: AccountRepositoryInterface,
        logs_repository: LogsRepositoryInterface,
        connection: DatabaseConnectionInterface,
    ):
        self.uuid = uuid
        self.account_repository = account_repository
        self.logs_repository = logs_repository
        self.connection = connection

    def execute(self) -> Response:
        try:
            while True:
                number = random.randint(100000, 999999)
                if not self.account_repository.get_by_number(number):
                    break

            while True:
                id = self.uuid.generate_uuid()
                if not self.account_repository.get_by_id(id):
                    break

            initial_balance = 10

            account = Account(
                id=id,
                number=number,
                balance=Decimal(initial_balance)
            )

            self.account_repository.create(account)

            self.connection.commit()

            save_logs = SaveLogs(self.logs_repository, self.uuid, self.connection)
            save_logs.execute(
                message=f"New account created: {number}",
                source_account=id,
                current_balance=initial_balance
            )

            return Response(
                content={
                    "account_number": number,
                    "initial_balance": initial_balance
                },
                status_code=200,
                error=False,
                context="Account created succesfully!"
            )

        except Exception as e:
            save_logs = SaveLogs(self.logs_repository, self.uuid, self.connection)
            save_logs.execute(
                message=f"ERROR while trying to create a new account: {getattr(e, 'message', str(e))}",
                source_account=id,
                error=True
            )
            print(getattr(e, 'log_message', str(e)))
            return Response(
                content={},
                status_code=getattr(e, 'code', 500),
                error=True,
                context=f"ERROR while trying to create a new account: {getattr(e, 'message', UNKNOWN_ERROR)}"
            )
