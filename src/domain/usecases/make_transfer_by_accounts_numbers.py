from decimal import Decimal
from domain.enums import BankTransactionType
from domain.errors import UNKNOWN_ERROR, AccountErrorHandler, InvalidDestinationAccountError
from domain.models import Response
from domain.ports import (
    AccountRepositoryInterface,
    DatabaseConnectionInterface,
    LogsRepositoryInterface,
    UuidInterface
)
from domain.services import SaveLogs


class MakeTransferByAccountsNumbers:
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

    def execute(
        self,
        source_account_number: int,
        transfer_value_amount: Decimal,
        destination_account_number: int
    ) -> Response:
        try:
            source_account = self.account_repository.get_by_number(source_account_number)
            AccountErrorHandler(
                source_account,
                BankTransactionType.TRANSFER.value,
                transfer_value_amount
            )

            if source_account_number == destination_account_number:
                raise InvalidDestinationAccountError(source_account_number)

            destination_account = self.account_repository.get_by_number(destination_account_number)
            AccountErrorHandler(
                destination_account,
                BankTransactionType.RECEIVE_TRANSFER.value,
                transfer_value_amount
            )

            source_account_new_balance = source_account.balance - transfer_value_amount

            self.account_repository.update_balance_by_id(
                source_account.id, source_account_new_balance
            )
            self.account_repository.update_balance_by_id(
                destination_account.id, destination_account.balance + transfer_value_amount
            )

            self.connection.commit()

            save_logs = SaveLogs(self.logs_repository, self.uuid, self.connection)
            save_logs.execute(
                message=f"Transfer completed",
                source_account=source_account.id,
                destination_account=destination_account.id,
                transaction_type=BankTransactionType.TRANSFER.value,
                current_balance=str(source_account_new_balance),
                transaction_amount=str(transfer_value_amount)
            )
            save_logs.execute(
                message=f"Transfer received",
                source_account=source_account.id,
                destination_account=destination_account.id,
                transaction_type=BankTransactionType.RECEIVE_TRANSFER.value,
                current_balance=str(destination_account.balance + transfer_value_amount),
                transaction_amount=str(transfer_value_amount)
            )

            return Response(
                content={
                    "current_balance": str(source_account_new_balance)
                },
                status_code=200,
                error=False,
                context="Transfer completed succesfully!"
            )

        except Exception as e:
            message = f"ERROR while trying to make a transfer: {getattr(e, 'message', str(e))}"
            save_logs = SaveLogs(self.logs_repository, self.uuid, self.connection)
            save_logs.execute(
                message=message,
                source_account=source_account_number,
                destination_account=destination_account_number,
                error=True,
                transaction_type=BankTransactionType.TRANSFER.value,
                transaction_amount=str(transfer_value_amount)
            )
            print(message)
            return Response(
                content={},
                status_code=getattr(e, 'code', 500),
                error=True,
                context=f"ERROR while trying to make a transfer: {getattr(e, 'message', UNKNOWN_ERROR)}"
            )
