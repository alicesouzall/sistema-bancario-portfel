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
    GetAllAccounts,
    GetStatementByAccountNumber
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
    description="Cria uma nova conta com o saldo inicial de R$ 0.00"
)
def create_new_account(
    request: Request
) -> JSONResponse:
    connection = request.app.state.connection

    create_new_account = CreateNewAccount(
        adapter_manager.uuid(),
        adapter_manager.account_repository(connection),
        adapter_manager.logs_repository(connection),
        connection,
    )

    response = create_new_account.execute()
    return JSONResponse(content=asdict(response), status_code=response.status_code)

@accounts_route.post("/deposit",
    description="Realiza um depósito na conta a partir do valor e do número da conta"
)
def make_deposit(
    deposit_request_model: MakeDepositRequestModel,
    request: Request
) -> JSONResponse:
    connection = request.app.state.connection

    make_deposit = MakeDepositByAccountNumber(
        adapter_manager.account_repository(connection),
        adapter_manager.logs_repository(connection),
        adapter_manager.uuid(),
        connection,
    )

    response = make_deposit.execute(deposit_request_model.account_number, deposit_request_model.amount)
    return JSONResponse(content=asdict(response), status_code=response.status_code)

@accounts_route.post("/withdrawal",
    description="Realiza um saque na conta a partir do número da conta e do valor"
)
def make_withdrawal(
    withdrawal_request_model: MakeWithdrawalRequestModel,
    request: Request
) -> JSONResponse:
    connection = request.app.state.connection

    make_withdrawal = MakeWithdrawalByAccountNumber(
        adapter_manager.account_repository(connection),
        adapter_manager.logs_repository(connection),
        adapter_manager.uuid(),
        connection
    )

    response = make_withdrawal.execute(
        withdrawal_request_model.account_number,
        withdrawal_request_model.amount
    )
    return JSONResponse(content=asdict(response), status_code=response.status_code)

@accounts_route.post("/transfer",
    description="""Realiza uma transfêrencia a partir do número
        da conta remetente, do número da conta de destino e do valor
        da transferência
    """
)
def make_transfer(
    transfer_request_model: MakeTransferRequestModel,
    request: Request
) -> JSONResponse:
    connection = request.app.state.connection

    make_transfer = MakeTransferByAccountsNumbers(
        adapter_manager.account_repository(connection),
        adapter_manager.logs_repository(connection),
        adapter_manager.uuid(),
        connection
    )

    response = make_transfer.execute(
        transfer_request_model.source_account_number,
        transfer_request_model.amount,
        transfer_request_model.destination_account_number,
    )
    return JSONResponse(content=asdict(response), status_code=response.status_code)

@accounts_route.get("/all",
    description="Obter todas as contas e seus respectivos saldos"
)
def get_all_accounts(
    request: Request
) -> JSONResponse:
    connection = request.app.state.connection

    get_all_accounts = GetAllAccounts(
        adapter_manager.account_repository(connection),
        adapter_manager.logs_repository(connection),
        adapter_manager.uuid(),
        connection
    )

    response = get_all_accounts.execute()
    return JSONResponse(content=asdict(response), status_code=response.status_code)

@accounts_route.get("/{account_number}",
    description="Obter uma conta e seu respectivo saldo a partir do número da conta"
)
def get_account_by_number(
    account_number: str,
    request: Request
) -> JSONResponse:
    connection = request.app.state.connection

    get_account = GetAccountByNumber(
        adapter_manager.account_repository(connection),
        adapter_manager.logs_repository(connection),
        adapter_manager.uuid(),
        connection
    )

    response = get_account.execute(account_number)
    return JSONResponse(content=asdict(response), status_code=response.status_code)

@accounts_route.get("/statement/{account_number}",
    description="Obter o extrato bancário de uma conta partir do número da conta"
)
def get_statement_by_account_number(
    account_number: str,
    request: Request
) -> JSONResponse:
    connection = request.app.state.connection

    get_statement = GetStatementByAccountNumber(
        adapter_manager.account_repository(connection),
        adapter_manager.logs_repository(connection),
        adapter_manager.uuid(),
        connection
    )

    response = get_statement.execute(account_number)
    return JSONResponse(content=asdict(response), status_code=response.status_code)
