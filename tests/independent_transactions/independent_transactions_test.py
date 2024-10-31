from decimal import Decimal
from dotenv import load_dotenv
import pytest

load_dotenv()

def test_make_deposit(account_repository, make_deposit_usecase, account123):
    make_deposit_usecase.execute(
        account123.number,
        Decimal('100'),
    )

    balance123 = account_repository.get_by_number(account123.number)

    assert balance123.balance == Decimal('100')

def test_make_withdrawal(make_withdrawal_usecase, account123, account_repository):
    make_withdrawal_usecase.execute(
        account123.number,
        Decimal(50),
    )

    balance123 = account_repository.get_by_number(account123.number)
    assert balance123.balance == Decimal(50)

def test_make_transfer(account_repository, make_transfer_usecase, account123, account456):
    make_transfer_usecase.execute(
        account123.number,
        Decimal(30),
        account456.number
    )

    balance123 = account_repository.get_by_number(account123.number)
    balance456 = account_repository.get_by_number(account456.number)

    assert balance123.balance == Decimal(20)
    assert balance456.balance == Decimal(30)
