from decimal import Decimal
from domain.models import Account

class AccountRepositoryInterface:
    def create(self, account: Account) -> None:
        raise NotImplementedError("Account")

    def delete_by_id(self, id: str) -> None:
        raise NotImplementedError("Account")

    def update_balance_by_id(self, id: str, balance: Decimal) -> None:
        raise NotImplementedError("Account")

    def get_by_number(self, number: str) -> Account | None:
        raise NotImplementedError("Account")

    def get_by_id(self, id: str) -> Account | None:
        raise NotImplementedError("Account")

    def get_all(self) -> list[Account] | None:
        raise NotImplementedError("Account")
