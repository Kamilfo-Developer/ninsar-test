import re

from aiogram.filters import Filter
from aiogram.types import Message


class TelegramUsername:
    def __init__(self, username: str):
        matches = re.match(
            r".*\B@(?=\w{5,32}\b)[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*.*", username
        )
        is_valid = matches

        if not is_valid:
            raise ValueError("Invalid Telegram username")

        self.value = username


class IntegersRangeFilter(Filter):
    def __init__(self, lower_bound: int, upper_bound: int) -> None:
        if lower_bound > upper_bound:
            raise ValueError(
                "Lower bound should be lower than or equal to higher bound"
            )

        self.allowed_valules = set(range(lower_bound, upper_bound + 1))
        print("Here")

    async def __call__(self, message: Message) -> bool:
        print(
            "message.text in self.allowed_valules",
            self.allowed_valules,
        )
        try:
            print("here", int(message.text) in self.allowed_valules)
            return int(message.text) in self.allowed_valules

        except ValueError:
            return False
