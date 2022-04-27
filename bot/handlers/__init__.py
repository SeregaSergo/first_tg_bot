from .admin import register_admin_handlers, register_admin_handlers_last
from .client import register_client_handlers, register_client_handlers_last
from .common import register_common_handlers
from load_all import dp, config, telebot


def register_all():
    register_common_handlers(dp, config.tg_bot.group_id, telebot)
    register_admin_handlers(dp, config.tg_bot.admin_id)
    register_client_handlers(dp)
    register_admin_handlers_last(dp, config.tg_bot.admin_id)
    register_client_handlers_last(dp)