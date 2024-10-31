from decimal import Decimal
from domain.enums import BankTransactionType
from domain.errors import UNKNOWN_ERROR, AccountErrorHandler
from domain.models import Response
from domain.services import SaveLogs
from domain.ports import (
    AccountRepositoryInterface,
    DatabaseConnectionInterface,
    LogsRepositoryInterface,
    UuidInterface
)


class MakeWithdrawalByAccountNumber:
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

    def execute(self, account_number: int, withdrawal_amount: Decimal) -> Response:
        try:
            account = self.account_repository.get_by_number(account_number)
            AccountErrorHandler().verify_account_exceptions(
                account,
                BankTransactionType.WITHDRAWAL.value,
                withdrawal_amount
            )

            new_balance = account.balance - withdrawal_amount

            self.account_repository.update_balance_by_id(account.id, new_balance)

            self.connection.commit()

            save_logs = SaveLogs(self.logs_repository, self.uuid, self.connection)
            save_logs.execute(
                message=f"Withdrawal executed",
                account_id=account.id,
                context={
                    "transaction_type": BankTransactionType.WITHDRAWAL.value,
                    "current_balance": str(new_balance),
                    "transaction_amount": str(withdrawal_amount)
                }
            )

            return Response(
                content={
                    "current_balance": str(new_balance)
                },
                status_code=200,
                error=False,
                context="Withdrawal completed succesfully!"
            )

        except Exception as e:
            self.connection.rollback()
            message = f"ERROR while trying to make a withdrawal: {getattr(e, 'message', str(e))}"
            save_logs = SaveLogs(self.logs_repository, self.uuid, self.connection)
            save_logs.execute(
                message=message,
                context={
                    "source_account_number": account_number,
                    "transaction_type": BankTransactionType.WITHDRAWAL.value,
                    "transaction_amount": str(withdrawal_amount)
                },
                status_code=getattr(e, 'code', 500),
            )
            print(message)
            return Response(
                content={},
                status_code=getattr(e, 'code', 500),
                error=True,
                context=f"ERROR while trying to make a withdrawal: {getattr(e, 'message', UNKNOWN_ERROR)}"
            )
