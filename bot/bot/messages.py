from bot.bot.game_service import PlayerProgress


class Messages:
    def __init__(self) -> None:
        pass

    def get_start_message(self, full_name: str) -> str:
        return (
            f"Привет, {full_name}, давай сыграем в игру!\n"
            f"У тебя есть возможность выбрать число.\nЯ её дам.\n"
            f"Нужно угадать число.\nЧИСЛО Я НЕ ДАМ!\n"
            f"P.S. Также у тебя есть опыт и уровень, "
            f"их можно посмотреть с помощью команды /progress.\n"
        )

    def get_user_already_exists_message(self) -> str:
        return "Привет снова! Если хочешь увидеть свой уровень и опыт, введи /progress."

    def get_progress_message(self, progress: PlayerProgress) -> str:
        return (
            f"На данный момент у тебя такая статистика: \n"
            f"Уровень: {progress.level}\n"
            f"XP до следующего уровня: {progress.expirience_to_level_up_left}"
        )

    def get_less_estimation_message(self) -> str:
        return "Ответ больше, чем правильный"

    def get_greater_estimation_message(self) -> str:
        return "Ответ меньше, чем правильный"

    def get_right_answer_message(self) -> str:
        return "Угадал! Впрочем, я загадал новое число. Сможешь угадать? :3"

    def get_incorrect_input_message(
        self, lower_bound: int, higher_bound: int
    ) -> str:
        return (
            f"Вводить можно только целые числа "
            f"в диапазоне от {lower_bound} до {higher_bound}."
        )

    def get_missing_username_message(self) -> str:
        return (
            "У тебя нет ника в Телеграме, создай его и тогда сможешь сыграть!"
        )
