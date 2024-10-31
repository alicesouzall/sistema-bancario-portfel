from decimal import Decimal
from domain.models import Account

class AccountRepositoryInterface:
    def create(self, account: Account) -> None:
        raise NotImplementedError("AccountRepository")

    def delete_by_id(self, id: str) -> None:
        raise NotImplementedError("AccountRepository")

    def update_balance_by_id(self, id: str, balance: Decimal) -> None:
        raise NotImplementedError("AccountRepository")

    def get_by_number(self, number: int) -> Account | None:
        raise NotImplementedError("AccountRepository")

    def get_by_id(self, id: str) -> Account | None:
        raise NotImplementedError("AccountRepository")

    def get_all(self) -> list[Account] | None:
        raise NotImplementedError("AccountRepository")
