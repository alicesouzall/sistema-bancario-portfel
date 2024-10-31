from domain.models import Logs


class LogsRepositoryInterface:
    def create(self, log: Logs) -> None:
        raise NotImplementedError("LogRepository")

    def get_statement_by_account_id(self, account_id: str) -> list[Logs] | None:
        raise NotImplementedError("LogRepository")
