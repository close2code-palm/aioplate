from typing import Any, Callable, Dict, Union
from aiogram import BaseMiddleware, types
from collections.abc import Awaitable


class SQLAlchemyRepo(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[
            [Union[types.Message, types.InlineQuery], Dict[str, Any]],
            Awaitable[Any],
        ],
        event: Union[types.Message, types.InlineQuery],
        data: Dict[str, Any],
    ):
        data["repo"] = ...
        await handler(event, data)
