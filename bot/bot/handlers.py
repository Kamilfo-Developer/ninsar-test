from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from bot.bot.game_service import (
    GuessNumberEstimation,
    GuessNumberGameService,
    UserAlreadyExists,
)
from bot.bot.messages import Messages
from bot.bot.settings import app_settings
from bot.bot.utils import IntegersRangeFilter

dp = Dispatcher()

messages = Messages()


@dp.message(CommandStart())
async def start_handler(message: Message):
    username = message.from_user.username

    if username is None:
        await message.answer(messages.get_missing_username_message())

        return

    game_service = GuessNumberGameService("@" + message.from_user.username)

    try:
        await game_service.init_player()
    except UserAlreadyExists:
        await message.answer(messages.get_user_already_exists_message())
        return

    await message.answer(
        messages.get_start_message(message.from_user.full_name)
    )


@dp.message(Command("progress"))
async def progress_handler(message: Message):
    game_service = GuessNumberGameService("@" + message.from_user.username)

    stats = await game_service.get_progress()

    await message.answer(messages.get_progress_message(stats))


@dp.message(
    IntegersRangeFilter(
        lower_bound=app_settings.GUESS_GAME_LOWER_BOUND,
        upper_bound=app_settings.GUESS_GAME_UPPER_BOUND,
    )
)
async def guessed_number_handler(message: Message):
    game_service = GuessNumberGameService("@" + message.from_user.username)

    estimation_result = await game_service.guess(int(message.text))

    match estimation_result:
        case GuessNumberEstimation.LESS:
            await message.answer(messages.get_greater_estimation_message())
        case GuessNumberEstimation.GREATER:
            await message.answer(messages.get_less_estimation_message())
        case GuessNumberEstimation.RIGHT_ANSWER:
            await message.answer(messages.get_right_answer_message())
        case _:
            raise ValueError(
                "Something went wrong since this message shouldn't have been achieved"
            )


@dp.message()
async def default_handler(message: Message):
    await message.answer(
        messages.get_incorrect_input_message(
            app_settings.GUESS_GAME_LOWER_BOUND,
            app_settings.GUESS_GAME_UPPER_BOUND,
        )
    )
