from dataclasses import dataclass
from datetime import datetime
from domain.enums import BankTransactionType


@dataclass
class Context:
    source_account: str
    destination_account: str | None
    transaction_type: BankTransactionType | None
    current_balance: str | None
    transaction_amount: str | None

@dataclass
class Logs:
    id: str
    error: bool
    context: Context
    message: str
    date: datetime
