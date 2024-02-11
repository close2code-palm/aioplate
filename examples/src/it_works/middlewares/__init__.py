from aiogram import Dispatcher
from .sql_alchemy_repo import SQLAlchemyRepo


def init_middles(dp: Dispatcher):
    sql_alchemy_repo_mw = SQLAlchemyRepo()
    dp.message.outer_middleware(sql_alchemy_repo_mw)
    dp.inline_query.outer_middleware(sql_alchemy_repo_mw)
