from decimal import Decimal
from domain.enums.bank_transaction_type import BankTransactionType
from domain.errors import UNKNOWN_ERROR, AccountErrorHandler
from domain.models import Response
from domain.ports import AccountRepositoryInterface, DatabaseConnectionInterface


class MakeDepositByAccountNumber:
    def __init__(
        self,
        account_repository: AccountRepositoryInterface,
        connection: DatabaseConnectionInterface,
    ):
        self.account_repository = account_repository
        self.connection = connection

    def execute(self, account_number: int, deposit_amount: Decimal) -> Response:
        try:
            account = self.account_repository.get_by_number(account_number)
            AccountErrorHandler(account, BankTransactionType.DEPOSIT.value, deposit_amount)

            new_balance = account.balance + deposit_amount
            self.account_repository.update_balance_by_id(account.id, new_balance)

            self.connection.commit()

            return Response(
                content={
                    "current_balance": new_balance
                },
                status_code=200,
                error=False,
                context="Deposit completed succesfully!"
            )

        except Exception as e:
            print(getattr(e, 'log_message', ""))
            return Response(
                content={},
                status_code=getattr(e, 'code', 500),
                error=True,
                context=f"ERROR while trying to make a deposit: {getattr(e, 'message', UNKNOWN_ERROR)}"
            )
