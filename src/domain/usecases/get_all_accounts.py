from domain.enums import BankTransactionType
from domain.errors import UNKNOWN_ERROR
from domain.models import Response
from domain.ports import AccountRepositoryInterface, DatabaseConnectionInterface


class GetAllAccounts:
    def __init__(
        self,
        account_repository: AccountRepositoryInterface,
        connection: DatabaseConnectionInterface,
    ):
        self.account_repository = account_repository
        self.connection = connection

    def execute(self) -> Response:
        try:
            accounts = self.account_repository.get_all()

            self.connection.commit()

            return Response(
                content=(
                    [
                        {
                            "number": a.number,
                            "balance": str(a.balance)
                        } for a in accounts
                    ] if accounts else []
                ),
                status_code=200,
                error=False,
                context="Accounts fetched succesfully!" if accounts else "No accounts found."
            )

        except Exception as e:
            self.connection.rollback()
            print(getattr(e, 'message', str(e)))
            return Response(
                content={},
                status_code=getattr(e, 'code', 500),
                error=True,
                context=f"ERROR while trying to get accounts: {getattr(e, 'message', UNKNOWN_ERROR)}"
            )
