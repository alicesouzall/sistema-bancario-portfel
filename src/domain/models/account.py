from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Account:
    id: str
    number: int
    balance: Decimal
