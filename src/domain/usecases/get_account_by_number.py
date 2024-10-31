from domain.errors import UNKNOWN_ERROR, AccountErrorHandler
from domain.models import Response
from domain.services import SaveLogs
from domain.ports import (
    AccountRepositoryInterface,
    DatabaseConnectionInterface,
    LogsRepositoryInterface,
    UuidInterface
)


class GetAccountByNumber:
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

    def execute(self, account_number: int) -> Response:
        try:
            account = self.account_repository.get_by_number(account_number)
            AccountErrorHandler().verify_account_exceptions(account)

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
            self.connection.rollback()
            message=f"ERROR while trying to get account {account_number}: {getattr(e, 'message', str(e))}"
            save_logs = SaveLogs(self.logs_repository, self.uuid, self.connection)
            save_logs.execute(
                message=message,
                context={
                    "account_number": account_number
                },
                status_code=getattr(e, 'code', 500)
            )
            print(message)
            return Response(
                content={},
                status_code=getattr(e, 'code', 500),
                error=True,
                context=f"ERROR while trying to get account by number: {getattr(e, 'message', UNKNOWN_ERROR)}"
            )
