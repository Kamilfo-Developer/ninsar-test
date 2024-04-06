from dataclasses import dataclass


@dataclass
class PlayerDTO:
    telegram_username: str
    right_answer: int
    expirience: int
    level: int
