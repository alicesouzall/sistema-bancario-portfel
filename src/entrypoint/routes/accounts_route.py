from dataclasses import asdict
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from domain.models import Response
from domain.usecases import (
    CreateNewAccount,
    MakeWithdrawalByAccountNumber,
    MakeDepositByAccountNumber,
    MakeTransferByAccountsNumbers,
    GetAccountByNumber,
    GetAllAccounts
)
from entrypoint.models import (
    MakeWithdrawalRequestModel,
    MakeDepositRequestModel,
    MakeTransferRequestModel
)
from infra import AdapterManager

accounts_route = APIRouter(
    prefix="/accounts",
    responses={
        404: {"description": "Not found"},
        200: {
            "description": "Account created successfully!",
            "content": {
                "application/json": {
                    "example": {
                        **asdict(Response(
                            {},
                            False,
                            200,
                            "Accounts routes"
                        ))
                    }
                }
            }
         }
    },
)

adapter_manager = AdapterManager()

@accounts_route.post("/",
    description="Create new account with initial balance"
)
def create_account_with_initial_balance(
    request: Request
) -> JSONResponse:
    connection = request.app.state.connection

    create_new_account = CreateNewAccount(
        adapter_manager.uuid(),
        adapter_manager.account_repository(connection),
        connection,
    )

    response = create_new_account.execute()
    return JSONResponse(content=asdict(response), status_code=response.status_code)

@accounts_route.post("/deposit",
    description="Make a deposit to the account by the account number"
)
def make_deposit(
    deposit_request_model: MakeDepositRequestModel,
    request: Request
) -> JSONResponse:
    connection = request.app.state.connection

    make_deposit = MakeDepositByAccountNumber(
        adapter_manager.account_repository(connection),
        connection
    )

    response = make_deposit.execute(deposit_request_model.account_number, deposit_request_model.amount)
    return JSONResponse(content=asdict(response), status_code=response.status_code)

@accounts_route.post("/withdrawal",
    description="Make a withdrawal from the account by the account number"
)
def make_withdrawal(
    withdrawal_request_model: MakeWithdrawalRequestModel,
    request: Request
) -> JSONResponse:
    connection = request.app.state.connection

    make_withdrawal = MakeWithdrawalByAccountNumber(
        adapter_manager.account_repository(connection),
        connection
    )

    response = make_withdrawal.execute(withdrawal_request_model.account_number, withdrawal_request_model.amount)
    return JSONResponse(content=asdict(response), status_code=response.status_code)

@accounts_route.post("/transfer",
    description="Make a transfer from the source account to the destination account by the acocounts numbers"
)
def make_transfer(
    transfer_request_model: MakeTransferRequestModel,
    request: Request
) -> JSONResponse:
    connection = request.app.state.connection

    make_transfer = MakeTransferByAccountsNumbers(
        adapter_manager.account_repository(connection),
        connection
    )

    response = make_transfer.execute(
        transfer_request_model.source_account_number,
        transfer_request_model.amount,
        transfer_request_model.destination_account_number,
    )
    return JSONResponse(content=asdict(response), status_code=response.status_code)

@accounts_route.get("/all",
    description="Get all accounts and their respective balances"
)
def get_all_accounts(
    request: Request
) -> JSONResponse:
    connection = request.app.state.connection

    get_all_accounts = GetAllAccounts(
        adapter_manager.account_repository(connection),
        connection
    )

    response = get_all_accounts.execute()
    return JSONResponse(content=asdict(response), status_code=response.status_code)

@accounts_route.get("/{account_number}",
    description="Get an account by the account number"
)
def get_account_by_number(
    account_number: str,
    request: Request
) -> JSONResponse:
    connection = request.app.state.connection

    get_account = GetAccountByNumber(
        adapter_manager.account_repository(connection),
        connection
    )

    response = get_account.execute(account_number)
    return JSONResponse(content=asdict(response), status_code=response.status_code)
