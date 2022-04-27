from .client import set_client_commands
from .admin import set_admin_commands

async def set_menus(bot):
    await set_admin_commands(bot)
    await set_client_commands(bot)