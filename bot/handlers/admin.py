from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter


#################################################################
############ Функции доступные только администратору ############
#################################################################

async def cmd_report(message: types.Message):
    await message.answer_document(types.InputFile('requirements.txt'), caption='Отчетные данные по опросу')

def register_admin_handlers(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(cmd_report, IDFilter(user_id=admin_id), commands="report")
    dp.register_message_handler(cmd_report, IDFilter(user_id=admin_id), commands="report")