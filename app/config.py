from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    ENV: str = "production"

    SQLALCHEMY_DATABASE_URI: PostgresDsn = "postgres://user:pass@localhost:5432/foobar"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
