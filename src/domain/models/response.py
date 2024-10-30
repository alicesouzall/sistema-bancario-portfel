from dataclasses import dataclass
from typing import Any


@dataclass
class Response:
    content: dict[str, Any] | list[str, Any]
    error: bool
    status_code: int
    context: str
