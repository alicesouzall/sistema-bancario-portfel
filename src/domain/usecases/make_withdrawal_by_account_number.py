from decimal import Decimal
from domain.enums.bank_transaction_type import BankTransactionType
from domain.errors import UNKNOWN_ERROR, AccountErrorHandler
from domain.models import Response
from domain.ports import AccountRepositoryInterface, DatabaseConnectionInterface


class MakeWithdrawalByAccountNumber:
    def __init__(
        self,
        account_repository: AccountRepositoryInterface,
        connection: DatabaseConnectionInterface,
    ):
        self.account_repository = account_repository
        self.connection = connection

    def execute(self, account_number: int, withdrawal_amount: Decimal) -> Response:
        try:
            account = self.account_repository.get_by_number(account_number)
            AccountErrorHandler(account, BankTransactionType.WITHDRAWAL.value, withdrawal_amount)

            new_balance = account.balance - withdrawal_amount

            self.account_repository.update_balance_by_id(account.id, new_balance)

            self.connection.commit()

            return Response(
                content={
                    "current_balance": str(new_balance)
                },
                status_code=200,
                error=False,
                context="Withdrawal completed succesfully!"
            )

        except Exception as e:
            print(getattr(e, 'log_message', ""))
            print(str(e))

            return Response(
                content={},
                status_code=getattr(e, 'code', 500),
                error=True,
                context=f"ERROR while trying to make a withdrawal: {getattr(e, 'message', UNKNOWN_ERROR)}"
            )