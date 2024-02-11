from pydantic import BaseModel
import os
from contextlib import suppress
from typing import TextIO


class Telegram(BaseModel):
    token: str


class SQLAlchemyRepo(BaseModel):
    db: str
    user: str
    password: str
    host: str
    port: int


class Config(BaseModel):
    telegram: Telegram
    sql_alchemy_repo: SQLAlchemyRepo


def parse_to_env(env_file: TextIO):
    for line in env_file.readlines():
        if "=" in line:
            k, v = line.split("=")
            os.environ[k] = v.strip()


def read_config(env_path: str | None = None) -> Config:
    if env_path:
        with suppress(FileNotFoundError):
            with open(env_path) as env_file:
                parse_to_env(env_file)
    telegram = Telegram(
        token=os.environ.get('TOKEN'),
    )
    sql_alchemy_repo = SQLAlchemyRepo(
        db=os.environ.get('DB'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        host=os.environ.get('HOST'),
        port=int(os.environ.get('PORT')),
    )
    return Config(
        telegram=telegram,
        sql_alchemy_repo=sql_alchemy_repo,
    )
