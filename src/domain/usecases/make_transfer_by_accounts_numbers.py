from decimal import Decimal
from domain.enums.bank_transaction_type import BankTransactionType
from domain.errors import UNKNOWN_ERROR, AccountErrorHandler
from domain.models import Response
from domain.ports import AccountRepositoryInterface, DatabaseConnectionInterface


class MakeTransferByAccountsNumbers:
    def __init__(
        self,
        account_repository: AccountRepositoryInterface,
        connection: DatabaseConnectionInterface,
    ):
        self.account_repository = account_repository
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

            return Response(
                content={
                    "current_balance": str(source_account_new_balance)
                },
                status_code=200,
                error=False,
                context="Transfer completed succesfully!"
            )

        except Exception as e:
            print(getattr(e, 'log_message', ""))
            return Response(
                content={},
                status_code=getattr(e, 'code', 500),
                error=True,
                context=f"ERROR while trying to make a transfer: {getattr(e, 'message', UNKNOWN_ERROR)}"
            )
