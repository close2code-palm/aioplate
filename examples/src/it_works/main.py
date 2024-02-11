from config import read_config
from aiogram import Bot, Dispatcher
from src.it_works.middlewares import init_middles
from src.it_works.routers import init_routers


def main():
    config = read_config(".env")
    bot = Bot(token=...)
    dp = Dispatcher()
    init_routers(dp)
    github_api_http_connector = ...
    dp["github_api_http_connector"] = github_api_http_connector
    init_middles(dp, config)
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
