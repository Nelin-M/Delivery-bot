"""
Implemented a class that does not allow the user to flood in the bot
"""
# pylint: disable-all

import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix="antiflood_"):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        on_process_message
        """
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    @staticmethod
    async def message_throttled(message: types.Message, throttled: Throttled):
        """
        message_throttled
        """

        # todo: refactor + текста
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count == 3:
            await message.reply("Вы отправляете слишком много сообщений, подождите несколько секунд.")
        elif throttled.exceeded_count == 4:
            await message.reply("Вы отправляете слишком много сообщений, подождите около 10 секунд.")
        await asyncio.sleep(delta)
