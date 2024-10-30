from dataclasses import dataclass


@dataclass
class Log:
    error: bool
    context: str
