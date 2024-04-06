from .services import (
    GuessGame,
    GuessGameService,
    PlayerDAO,
    PlayerExpirienceCalculator,
)


def get_guess_game_service() -> GuessGameService:
    guess_game = GuessGame()
    player_dao = PlayerDAO()
    player_expirience_calculator = PlayerExpirienceCalculator()

    guess_game_service = GuessGameService(
        guess_game, player_expirience_calculator, player_dao
    )

    return guess_game_service
