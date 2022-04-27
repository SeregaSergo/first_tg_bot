from aiogram.types import BotCommandScopeDefault
from aiogram import Bot


async def delete_menu(bot: Bot):
    await bot.delete_my_commands(BotCommandScopeDefault())