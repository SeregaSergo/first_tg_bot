from aiogram.types import BotCommand, BotCommandScopeChatAdministrators
from aiogram import Bot
from load_all import config


async def set_admin_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать опрос"),
        BotCommand(command="/previous", description="Предыдущий вопрос"),
        BotCommand(command="/interrupt", description="Закончить опрос"),
        BotCommand(command="/list_reports", description="Список отчетов"),
        BotCommand(command="/report_current", description="Получить новый отчет")
    ]
    scope = BotCommandScopeChatAdministrators(config.tg_bot.group_id)
    await bot.set_my_commands(commands, scope)