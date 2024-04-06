import json
from dataclasses import dataclass
from enum import Enum

from httpx import AsyncClient

from bot.bot.settings import app_settings
from bot.bot.utils import TelegramUsername


class UserAlreadyExists(Exception):
    pass


@dataclass
class PlayerProgress:
    level: int
    expirience_to_level_up_left: int


@dataclass
class GuessNumberPlayerChoice:
    number: int


@dataclass
class GuessNumberRightAnswer:
    right_answer: int


class GuessNumberEstimation(Enum):
    LESS = "LESS"
    RIGHT_ANSWER = "RIGHT_ANSWER"
    GREATER = "GREATER"


@dataclass
class GuessResult:
    estimation: GuessNumberEstimation

    def to_json(self):
        return json.dumps({"estimation": self.estimation})


class GuessNumberGameService:
    def __init__(self, telegram_username: str):
        self.telegram_username = TelegramUsername(telegram_username)

        self.API_URL_PATH_PREFIX = app_settings.API_URL_PREFIX + "/api/v1/"

    # Отправление ответа на задачку,
    # в случае успешного ответа прибавлять опыт (количество опыта за верный ответ на
    # выбор соискателя) и присылать юзеру текущий уровень и оставшийся опыт.
    async def __send_number(self, number: int):
        async with AsyncClient() as client:
            response = await client.post(
                self.API_URL_PATH_PREFIX + "answer",
                json={
                    "telegram_username": self.telegram_username.value,
                    "number": number,
                },
            )

            parsed = response.json()

            return parsed

    async def guess(self, guessed_number: int) -> GuessNumberEstimation:
        queried_result = await self.__send_number(guessed_number)

        estimation = queried_result.get("estimation")

        match estimation:
            case "LESS":
                return GuessNumberEstimation.LESS
            case "GREATER":
                return GuessNumberEstimation.GREATER
            case "RIGHT_ANSWER":
                return GuessNumberEstimation.RIGHT_ANSWER
            case _:
                raise ValueError(
                    "Something went wrong since "
                    "this message shouldn't have been achieved"
                )

    async def init_player(
        self,
    ):
        async with AsyncClient() as client:
            response = await client.post(
                self.API_URL_PATH_PREFIX + "players",
                json={"telegram_username": self.telegram_username.value},
            )

            if response.status_code == 409:
                raise UserAlreadyExists()

    async def __query_progress(self) -> dict:
        async with AsyncClient() as client:
            response = await client.get(
                self.API_URL_PATH_PREFIX
                + "players/"
                + f"{self.telegram_username.value}"
            )

        parsed = response.json()

        return parsed

    async def get_progress(self) -> PlayerProgress:
        queried_progress = await self.__query_progress()

        try:
            result = PlayerProgress(
                level=queried_progress["level"],
                expirience_to_level_up_left=queried_progress[
                    "expirience_to_level_up_left"
                ],
            )

            return result

        except KeyError:
            raise ValueError(
                "Something went wrong since "
                "this message shouldn't have been reached"
            )
