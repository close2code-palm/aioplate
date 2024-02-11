from aiogram import Router, types
from aiogram.fsm.context import FSMContext


intro_router = Router()


@intro_router.message()
async def start_handler(message: types.Message):
    ...


@intro_router.message()
async def save_me(message: types.Message, repo: ...):
    ...


@intro_router.callback_query()
async def dumb_state(call: types.CallbackQuery, state: FSMContext):
    ...
