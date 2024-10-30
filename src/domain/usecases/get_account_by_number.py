from decimal import Decimal
from domain.enums.bank_transaction_type import BankTransactionType
from domain.errors import UNKNOWN_ERROR, AccountErrorHandler
from domain.models import Response
from domain.ports import AccountRepositoryInterface, DatabaseConnectionInterface


class GetAccountByNumber:
    def __init__(
        self,
        account_repository: AccountRepositoryInterface,
        connection: DatabaseConnectionInterface,
    ):
        self.account_repository = account_repository
        self.connection = connection

    def execute(self, account_number: int) -> Response:
        try:
            account = self.account_repository.get_by_number(account_number)
            AccountErrorHandler(account)

            self.connection.commit()

            return Response(
                content={
                    "number": account.number,
                    "balance": str(account.balance)
                },
                status_code=200,
                error=False,
                context="Account fetched succesfully!"
            )

        except Exception as e:
            print(getattr(e, 'log_message', ""))
            return Response(
                content={},
                status_code=getattr(e, 'code', 500),
                error=True,
                context=f"ERROR while trying to get account by number: {getattr(e, 'message', UNKNOWN_ERROR)}"
            )
