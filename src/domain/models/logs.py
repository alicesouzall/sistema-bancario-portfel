from dataclasses import dataclass
from datetime import datetime

@dataclass
class Logs:
    id: str
    status_code: int
    message: str
    date: datetime
    account_id: str | None
    context: dict[str, str] | None
