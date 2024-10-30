from dataclasses import asdict
from decimal import Decimal
from domain.models import Account
from domain.ports import AccountRepositoryInterface
from infra.adapter.database import DatabaseConnection

class AccountRepositoryPostgres(AccountRepositoryInterface):
    connection: DatabaseConnection

    def __init__(self, connection: DatabaseConnection) -> None:
        self.connection = connection

    def create(self, account: Account) -> None:
        query = """
            INSERT INTO account (id, number, balance)
            VALUES (%(id)s, %(number)s, %(balance)s);
        """
        self.connection.execute_query(query, asdict(account))

    def delete_by_id(self, id: str) -> None:
        query = """
            DELETE FROM account WHERE id = %s;
        """
        self.connection.execute_query(query, (id,))

    def update_balance_by_id(self, id: str, balance: Decimal) -> None:
        query = """
            UPDATE account SET balance = %s
            WHERE id = %s;
        """
        self.connection.execute_query(query, (balance, id))

    def get_by_number(self, number: str) -> Account | None:
        query = """
            SELECT * FROM account WHERE number = %s;
        """
        response = self.connection.execute_query(query, (number,))
        return Account(**response[0]) if response else None

    def get_by_id(self, id: str) -> Account | None:
        query = """
            SELECT * FROM account WHERE id = %s;
        """
        response = self.connection.execute_query(query, (id,))
        return Account(**response[0]) if response else None

    def get_all(self) -> list[Account] | None:
        query = """
            SELECT * FROM account;
        """
        response = self.connection.execute_query(query)
        return [Account(**a) for a in response] if response else None
