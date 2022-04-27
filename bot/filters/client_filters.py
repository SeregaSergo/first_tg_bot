from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException


class isNotPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type != types.ChatType.PRIVATE


class isNotMember(BoundFilter):

    def __init__(self, group_id, telebot):
    
        self.group_id: int = group_id
        self.bot: TeleBot = telebot

    async def check(self, message: types.Message):
        try:
            if self.bot.get_chat_member(self.group_id, message.from_user.id).status == "left":
                return True
        except (ApiTelegramException):
            return False