from decimal import ROUND_DOWN, Decimal
from pydantic import BaseModel, field_validator


class MakeTransferRequestModel(BaseModel):
    source_account_number: int
    destination_account_number: int
    amount: Decimal

    @field_validator('amount')
    def round_to_two_decimal_places(cls, value):
        return Decimal(value).quantize(Decimal("0.00"), rounding=ROUND_DOWN)
