from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters.builtin import Text
from .dbworker import db
from .common import phrases


#################################################################
############ Функции доступные только администратору ############
#################################################################


class ReportState(StatesGroup):
    waiting_for_answer = State()
    final = State()


async def cmd_report_all(message: types.Message):
    db.get_report()
    await message.answer_document(types.InputFile('requirements.txt'), caption='Отчетные данные по опросу')


async def cmd_report_cur(message: types.Message):
    # file_path, date = await db.create_report()
    # await message.answer_document(
    #     types.InputFile(file_path), 
    #     caption=f'Промежуточные данные по текущему опросу (старт {date})'
    # )
    pass


async def cmd_help_adm(message: types.Message):
    await message.answer(phrases.START_HELP_ADM)


def register_admin_handlers(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(cmd_report_all, user_id=admin_id, commands="list_reports")
    dp.register_message_handler(cmd_report_cur, user_id=admin_id, commands="report_current")
    

def register_admin_handlers_last(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(cmd_help_adm, user_id=admin_id, state=None)