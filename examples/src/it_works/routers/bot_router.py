from aiogram import Router, types, Bot


bot_router = Router()


@bot_router.inline_query()
async def dumb_bot(inline: types.InlineQuery, repo: ..., bot: Bot):
    ...
