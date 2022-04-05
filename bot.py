import asyncio
import logging
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config.config_reader import load_config
from questions import questions as q
from handlers.admin import register_admin_handlers
from handlers.client import register_client_handlers
from db_dir import dbworker as db


logger = logging.getLogger(__name__)

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/previous", description="Предыдущий вопрос"),
        BotCommand(command="/interrupt", description="Закончить опрос")
    ]
    await bot.set_my_commands(commands)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


async def main():
    # Парсинг файла конфигурации
    config = load_config("config/bot.ini")
    
    # Инициализация БД
    db.start_db()

    # Инициализация списка вопросов
    q.initialize()
    
    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger.info("Starting bot: {bot_name}".format(bot_name = (await bot.get_me()).username))

    # Регистрация хэндлеров
    register_admin_handlers(dp, config.tg_bot.admin_id)
    register_client_handlers(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    await dp.skip_updates()  # пропуск накопившихся апдейтов
    await dp.start_polling()
    await shutdown(dp)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
