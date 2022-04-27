from aiogram.types import BotCommand, BotCommandScope, BotCommandScopeAllPrivateChats
from aiogram import Bot


async def set_client_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать опрос"),
        BotCommand(command="/previous", description="Предыдущий вопрос"),
        BotCommand(command="/interrupt", description="Закончить опрос")
    ]
    scope = BotCommandScopeAllPrivateChats()
    await bot.set_my_commands(commands, scope)