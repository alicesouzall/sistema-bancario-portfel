from enum import Enum

class BankTransactionType(Enum):
    TRANSFER = "TRANSFER"
    RECEIVE_TRANSFER = "RECEIVE TRANSFER"
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
