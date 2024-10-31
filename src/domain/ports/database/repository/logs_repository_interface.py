from domain.models import Logs


class LogsRepositoryInterface:
    def create(self, log: Logs) -> None:
        raise NotImplementedError("LogRepository")
