from decimal import Decimal
from domain.enums import BankTransactionType
from domain.errors import UNKNOWN_ERROR, AccountErrorHandler
from domain.models import Response
from domain.ports import (
    AccountRepositoryInterface,
    DatabaseConnectionInterface,
    LogsRepositoryInterface,
    UuidInterface
)
from domain.services import SaveLogs


class MakeDepositByAccountNumber:
    def __init__(
        self,
        account_repository: AccountRepositoryInterface,
        logs_repository: LogsRepositoryInterface,
        uuid: UuidInterface,
        connection: DatabaseConnectionInterface,
    ):
        self.account_repository = account_repository
        self.logs_repository = logs_repository
        self.uuid = uuid
        self.connection = connection

    def execute(self, account_number: int, deposit_amount: Decimal) -> Response:
        try:
            account = self.account_repository.get_by_number(account_number)
            AccountErrorHandler(account, BankTransactionType.DEPOSIT.value, deposit_amount)

            new_balance = account.balance + deposit_amount
            self.account_repository.update_balance_by_id(account.id, new_balance)

            self.connection.commit()

            save_logs = SaveLogs(self.logs_repository, self.uuid, self.connection)
            save_logs.execute(
                message=f"Deposit executed",
                source_account=account.id,
                transaction_type=BankTransactionType.DEPOSIT.value,
                current_balance=str(new_balance),
                transaction_amount=str(deposit_amount)
            )

            return Response(
                content={
                    "current_balance": str(new_balance)
                },
                status_code=200,
                error=False,
                context="Deposit completed succesfully!"
            )

        except Exception as e:
            message = f"ERROR while trying to make a deposit: {getattr(e, 'message', str(e))}"
            save_logs = SaveLogs(self.logs_repository,self.uuid,  self.connection)
            save_logs.execute(
                message=message,
                source_account=account_number,
                error=True,
                transaction_type=BankTransactionType.DEPOSIT.value,
                transaction_amount=str(deposit_amount)
            )
            print(message)
            return Response(
                content={},
                status_code=getattr(e, 'code', 500),
                error=True,
                context=f"ERROR while trying to make a deposit: {getattr(e, 'message', UNKNOWN_ERROR)}"
            )
