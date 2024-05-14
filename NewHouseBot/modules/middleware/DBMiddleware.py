from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import Message

from NewHouseBot.modules.other.Request import Request

class DbSession(BaseMiddleware):
    def __init__(self, connector):
        self.connector = connector

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        data['request'] = Request(self.connector.cursor())
        return await handler(event, data)
