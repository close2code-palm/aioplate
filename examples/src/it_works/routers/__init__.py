from aiogram import Dispatcher
from .intro_router import intro_router
from .bot_router import bot_router


def init_routers(dp: Dispatcher):
    dp.include_routers(intro_router, bot_router,)
