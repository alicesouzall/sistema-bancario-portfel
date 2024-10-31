from decimal import Decimal
from dotenv import load_dotenv
import pytest
from domain.models import Account
from domain.usecases import (
    MakeDepositByAccountNumber,
    MakeTransferByAccountsNumbers,
    MakeWithdrawalByAccountNumber
)
from infra import AdapterManager
from infra.adapter.database import DatabaseFactory

load_dotenv()

def setup_accounts(database_connection, accounts, account_repository):
    for account in accounts:
        account_repository.create(account)

    database_connection.commit()

@pytest.fixture(scope="module")
def uuid():
    return AdapterManager().uuid()

@pytest.fixture(scope="module")
def account123(uuid):
    return Account(
        uuid.generate_uuid(),
        "123",
        Decimal(0)
    )

@pytest.fixture(scope="module")
def account456(uuid):
    return Account(
        uuid.generate_uuid(),
        "456",
        Decimal(0)
    )

@pytest.fixture(scope="module")
def accounts(account123, account456):
    return [
        account123, account456
    ]

@pytest.fixture(scope="module")
def database_connection(accounts):
    with DatabaseFactory().create_postgres_connection() as connection:
        yield connection

        for account in accounts:
            AdapterManager().account_repository(connection).delete_by_id(account.id)
            connection.commit()

@pytest.fixture(scope="module")
def account_repository(database_connection, accounts):
    repository = AdapterManager().account_repository(database_connection)
    setup_accounts(database_connection, accounts, repository)
    return repository

@pytest.fixture(scope="module")
def logs_repository(database_connection):
    return AdapterManager().logs_repository(database_connection)

@pytest.fixture(scope="module")
def make_deposit_usecase(database_connection, account_repository, uuid, logs_repository):
    return MakeDepositByAccountNumber(
        account_repository,
        logs_repository,
        uuid,
        database_connection
    )

@pytest.fixture(scope="module")
def make_transfer_usecase(database_connection, account_repository, uuid, logs_repository):
    return MakeTransferByAccountsNumbers(
        account_repository,
        logs_repository,
        uuid,
        database_connection
    )

@pytest.fixture(scope="module")
def make_withdrawal_usecase(database_connection, account_repository, uuid, logs_repository):
    return MakeWithdrawalByAccountNumber(
        account_repository,
        logs_repository,
        uuid,
        database_connection
    )
