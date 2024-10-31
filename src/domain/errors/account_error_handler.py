from decimal import Decimal
from domain.enums import BankTransactionType
from domain.models import Account

ACCOUNT_DOES_NOT_EXIST_ERROR = "The %s account does not exist."
INSUFFICIENT_BALANCE_ERROR = "Insufficient balance at account %s"
INVALID_TRANSACTION_VALUE_ERROR = "Invalid value for transaction: %s"
INVALID_DESTINATION_ACCOUNT_ERROR = "Invalid destination account at account %s: you can't make a transfer to yourself"

class AccountErrorHandler:
    def verify_account_exceptions(
        self,
        account: Account | None,
        transaction_type: BankTransactionType = "",
        value: Decimal = Decimal(0),
    ):
        if not account:
            match transaction_type:
                case BankTransactionType.RECEIVE_TRANSFER.value:
                    message = ACCOUNT_DOES_NOT_EXIST_ERROR % ("destination",)
                case BankTransactionType.TRANSFER.value:
                    message = ACCOUNT_DOES_NOT_EXIST_ERROR % ("source",)
                case _:
                    message = ACCOUNT_DOES_NOT_EXIST_ERROR % ("",)
            raise AccountNotFoundError(message)
        if (
            transaction_type != BankTransactionType.DEPOSIT.value
            and transaction_type != BankTransactionType.RECEIVE_TRANSFER.value
            and account.balance < value
        ):
            raise InsufficientBalanceError(value, account, transaction_type)
        if value <= 0 and transaction_type:
            raise InvalidTransactionValueError(value, account, transaction_type)


class AccountNotFoundError(Exception):
    def __init__(self, message: str, code = 404):
        self.message = message
        self.code = code
        super().__init__(message, code)

class InsufficientBalanceError(Exception):
    def __init__(self, value: Decimal, account: Account, transaction_type: BankTransactionType):
        self.message = INSUFFICIENT_BALANCE_ERROR % (account.number,)
        super().__init__(value, account, transaction_type)

class InvalidTransactionValueError(Exception):
    def __init__(self, value: Decimal, account: Account, transaction_type: BankTransactionType):
        self.message = INVALID_TRANSACTION_VALUE_ERROR % (value,)
        super().__init__(value, account, transaction_type)

class InvalidDestinationAccountError(Exception):
    def __init__(self, account_number: int):
        self.message = INVALID_DESTINATION_ACCOUNT_ERROR % (account_number,)
        super().__init__(account_number)
