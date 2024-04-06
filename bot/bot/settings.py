from pydantic_settings import BaseSettings, SettingsConfigDict

PATH_TO_DOTENV_FILE = ".env"


class AppSettings(BaseSettings):
    BOT_TOKEN: str

    API_URL_PREFIX: str = "http://localhost:8000"

    GUESS_GAME_UPPER_BOUND: int
    GUESS_GAME_LOWER_BOUND: int

    model_config = SettingsConfigDict(
        env_file=PATH_TO_DOTENV_FILE, env_file_encoding="utf-8", extra="allow"
    )


app_settings = AppSettings()  # type: ignore
