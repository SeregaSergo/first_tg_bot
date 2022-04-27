from datetime import datetime
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from .dbworker import db, survey_dict
from .common import phrases


###################################################
############ Функции доступные клиенту ############
###################################################


class SurveyState(StatesGroup):
    waiting_for_answer = State()
    final = State()


final_keyboard = ReplyKeyboardMarkup(
                        keyboard=[[KeyboardButton(text="Закончить опрос"),
                        KeyboardButton(text="Предыдущий вопрос")]],
                        resize_keyboard=True
                 )


async def get_cur_question(state: FSMContext):
    async with state.proxy() as data:
        index = data["cur_question"]
        if survey_dict.get(data["id_survey"]) is None:
            await db.add_survey_to_active(data["id_survey"])
        return (index, survey_dict[data["id_survey"]][index])


async def save_answer(state: FSMContext, id_opt: int, user_id: int):
    async with state.proxy() as data:
        data["answers"].append((id_opt, user_id, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))


async def incr_question(state: FSMContext):
    async with state.proxy() as data:
        data["cur_question"] += 1
        if data["cur_question"] == data["num_q"]:
            return False
        else:
            return True
            

async def decr_question(state: FSMContext):
    async with state.proxy() as data:
        if data["cur_question"] != 0:
            data["cur_question"] -= 1
            data["answers"].pop()       
    if await state.get_state() == SurveyState.final.state:
        await SurveyState.waiting_for_answer.set()


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    num_q = await db.get_survey(message.from_user.id, state)   # checks what survey is last/how many questions are not answered 
    if num_q == 0:
        await message.answer(phrases.NO_QUESTION, reply_markup=types.ReplyKeyboardRemove())
    else:
        ending_part = "ов"
        if 1 < num_q < 5:
            ending_part = "а"
        elif num_q == 1:
            ending_part = ""
        await message.answer(phrases.WELCOME.format(num_q, ending_part))
        await SurveyState.waiting_for_answer.set()
        i_q, active_question = await get_cur_question(state)
        await message.answer("{}) {}".format(i_q + 1, active_question.question), \
                            reply_markup=active_question.keyboard)


async def get_answer(message: types.Message, state: FSMContext):
    i_q, active_question = await get_cur_question(state)
    opt = active_question.check_option(message.text)
    if opt == None:
        await message.answer(phrases.INCORRECT_ANSWER)
        return
    else:
        await save_answer(state, opt.id, message.from_user.id)
        if (await incr_question(state)):
            i_q, active_question = await get_cur_question(state)
            await message.answer("{}) {}".format(i_q + 1, active_question.question), \
                            reply_markup=active_question.keyboard)
        else:
            await SurveyState.final.set()
            await message.answer(phrases.END_OF_QUESTIONS, reply_markup=final_keyboard)


async def end_survey(message: types.Message, state: FSMContext):

    await message.answer(phrases.END_OF_SURVEY, reply_markup=types.ReplyKeyboardRemove())
    async with state.proxy() as data:
        await db.record_answers_db(data["answers"])
        if data["num_surveys"] < len(survey_dict):
            await message.answer(phrases.ONE_MORE_SURVEY)
    await state.finish()


async def cmd_previous(message: types.Message, state: FSMContext):
    await decr_question(state)
    i_q, active_question = await get_cur_question(state)
    await message.answer("{}) {}".format(i_q + 1, active_question.question), \
                            reply_markup=active_question.keyboard)


async def cmd_interrupt_survey(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(phrases.END_OF_SURVEY)
    

async def cmd_help(message: types.Message):
    await message.answer(phrases.START_HELP)


def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state=None)
    dp.register_message_handler(cmd_previous, commands="previous", state=SurveyState)
    dp.register_message_handler(cmd_interrupt_survey, commands="interrupt", state=SurveyState)
    dp.register_message_handler(cmd_previous, Text(equals="Предыдущий вопрос"), state="*")
    dp.register_message_handler(end_survey, Text(equals="Закончить опрос"), state=SurveyState.final)
    dp.register_message_handler(get_answer, state=SurveyState.waiting_for_answer)


def register_client_handlers_last(dp: Dispatcher):
    dp.register_message_handler(cmd_help, state=None)