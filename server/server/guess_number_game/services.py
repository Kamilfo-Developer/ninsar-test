import random
from dataclasses import dataclass
from enum import Enum

from server.settings import (
    EXPIRIENCE_PER_RIGHT_ANSWER,
    GUESS_GAME_LOWER_BOUND,
    GUESS_GAME_UPPER_BOUND,
)

from .dtos import PlayerDTO
from .models import Player


@dataclass
class PlayerExpirience:
    expirience: int
    level: int


@dataclass
class PlayerProgressDTO:
    expirience_to_level_up_left: int
    level: int


class GuessNumberEstimation(Enum):
    LESS = "LESS"
    RIGHT_ANSWER = "RIGHT_ANSWER"
    GREATER = "GREATER"


class NoSuchPlayer(Exception):
    pass


class PlayerAlreadyExists(Exception):
    pass


class PlayerExpirienceCalculator:
    EXPIRIENCE_PER_RIGHT_ANSWER = EXPIRIENCE_PER_RIGHT_ANSWER

    def __init__(self):
        pass

    def __calculate_player_expirience(
        self, player_expirience: int, player_level: int
    ) -> PlayerExpirience:

        new_expirience = player_expirience

        if new_expirience >= player_level * 100:
            new_expirience = 0
            player_level += 1

        return PlayerExpirience(new_expirience, player_level)

    def answer_correct(
        self, player_expirience: PlayerExpirience
    ) -> PlayerExpirience:
        new_expirience = (
            player_expirience.expirience + self.EXPIRIENCE_PER_RIGHT_ANSWER
        )

        return self.__calculate_player_expirience(
            new_expirience, player_expirience.level
        )

    def get_expirience_to_level_up(
        self, player_expirience: PlayerExpirience
    ) -> int:
        return player_expirience.level * 100 - player_expirience.expirience


class GuessGame:
    GUESS_GAME_LOWER_BOUND = GUESS_GAME_LOWER_BOUND
    GUESS_GAME_UPPER_BOUND = GUESS_GAME_UPPER_BOUND

    def __init__(self):
        pass

    def create_new_right_answer(self) -> int:
        return random.randint(GUESS_GAME_LOWER_BOUND, GUESS_GAME_UPPER_BOUND)

    def guess_number(
        self, guess_number: int, right_answer: int
    ) -> GuessNumberEstimation:

        if guess_number < right_answer:
            return GuessNumberEstimation.LESS

        if guess_number > right_answer:
            return GuessNumberEstimation.GREATER

        return GuessNumberEstimation.RIGHT_ANSWER


class PlayerDAO:
    def create_new_player(self, player_dto: PlayerDTO):
        try:
            Player.objects.get(telegram_username=player_dto.telegram_username)

            raise PlayerAlreadyExists("Player already exists")

        except Player.DoesNotExist:
            new_player = Player.from_dto(player_dto)

            new_player.save()

    def get_player_by_username(self, telegram_username: str) -> PlayerDTO:
        try:
            result = Player.objects.get(telegram_username=telegram_username)

            return result.as_dto()

        except Player.DoesNotExist:
            raise NoSuchPlayer("Player not found")

    def update_player(self, player_dto: PlayerDTO) -> None:
        try:
            player = Player.objects.get(
                telegram_username=player_dto.telegram_username
            )
        except Player.DoesNotExist:
            raise NoSuchPlayer("Player not found")

        player.right_answer = player_dto.right_answer
        player.level = player_dto.level
        player.expirience = player_dto.expirience

        player.save()


class GuessGameService:
    def __init__(
        self,
        guess_game: GuessGame,
        player_expirience_calculator: PlayerExpirienceCalculator,
        player_dao: PlayerDAO,
    ) -> None:
        self.__guess_game = guess_game
        self.__player_expirience_calculator = player_expirience_calculator
        self.__player_dao = player_dao

    def __win_game(self, player: PlayerDTO):
        new_player_expirience = (
            self.__player_expirience_calculator.answer_correct(
                PlayerExpirience(player.expirience, player.level)
            )
        )

        new_right_answer = self.__guess_game.create_new_right_answer()

        player.right_answer = new_right_answer
        player.level = new_player_expirience.level
        player.expirience = new_player_expirience.expirience

        self.__player_dao.update_player(player_dto=player)

    def create_new_player(self, telegram_username: str):
        player = PlayerDTO(
            telegram_username=telegram_username,
            right_answer=self.__guess_game.create_new_right_answer(),
            expirience=0,
            level=0,
        )

        self.__player_dao.create_new_player(player)

    def get_progress(self, telegram_username: str) -> PlayerProgressDTO:
        player = self.__player_dao.get_player_by_username(telegram_username)

        player_expirience = PlayerExpirience(player.expirience, player.level)

        expirience_to_level_up = (
            self.__player_expirience_calculator.get_expirience_to_level_up(
                player_expirience
            )
        )
        level = player_expirience.level

        return PlayerProgressDTO(
            expirience_to_level_up_left=expirience_to_level_up,
            level=level,
        )

    def check_answer(
        self, number: int, telegram_username: str
    ) -> GuessNumberEstimation:
        player = self.__player_dao.get_player_by_username(telegram_username)

        estimation = self.__guess_game.guess_number(
            number, player.right_answer
        )

        if estimation == GuessNumberEstimation.RIGHT_ANSWER:
            self.__win_game(player)

        return estimation
