from aiogram import executor, Dispatcher, Bot

import handlers
import filters
from load_all import config, bot, dp
from menus import set_menus


async def on_startup(dispatcher: Dispatcher):

    # Связывание фильтров для хендлеров с диспетчером
    filters.setup(dp)

    # Регистрация хэндлеров
    handlers.register_all()

    await set_menus(bot)

    # Оповещение о запуске бота
    await bot.send_message(config.tg_bot.admin_id, "Я запущен!")


async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.close()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown, on_startup=on_startup)
