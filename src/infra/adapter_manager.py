from infra.adapter.database import *
from infra.adapter.database import *
from domain.ports import *

class AdapterManager:
    def uuid(self) -> UuidInterface:
        return Uuid()

    def account_repository(self, connection: DatabaseConnectionInterface) -> AccountRepositoryInterface:
        return AccountRepositoryPostgres(connection)

    def logs_repository(self, connection: DatabaseConnectionInterface) -> LogsRepositoryInterface:
        return LogsRepositoryPostgres(connection)
