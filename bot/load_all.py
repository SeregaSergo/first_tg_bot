import asyncio
import logging
from config import Config
from telebot import TeleBot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher


# Настройка логирования в stdout
logger = logging.getLogger("bot")
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Парсинг файла конфигурации
config = Config("config/bot.ini")

# Storage для хранения состояний FSM
storage = MemoryStorage()

# Объявление и инициализация объектов бота и диспетчера
bot = Bot(token=config.tg_bot.token)
telebot = TeleBot(config.tg_bot.token)
dp = Dispatcher(bot, storage=storage)