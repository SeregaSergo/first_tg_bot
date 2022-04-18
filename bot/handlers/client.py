from datetime import datetime
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from questions.questions import survey_dict
from db_dir.dbworker import get_survey, record_answers_db
from keyboards.keyboards import final_keyboard


class SurveyState(StatesGroup):
    waiting_for_answer = State()
    final = State()

###################################################
############ Функции доступные клиенту ############
###################################################


async def get_cur_question(state: FSMContext):
    async with state.proxy() as data:
        index = data["cur_question"]
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
    num_q = await get_survey(message.from_user.id, state)   # checks what survey is last/how many questions are not answered 
    if num_q == 0:
        await message.answer("У нас не осталось к вам вопросов!",
                                reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer(
            "У нас есть к вам {} вопрос{}!".format(num_q, 
                        "a" if (0 < num_q < 5) else "ов")
        )
        await SurveyState.waiting_for_answer.set()
        i_q, active_question = await get_cur_question(state)
        await message.answer("{}) {}".format(i_q + 1, active_question.question), \
                            reply_markup=active_question.keyboard)


async def get_answer(message: types.Message, state: FSMContext):
    i_q, active_question = await get_cur_question(state)
    opt = active_question.check_option(message.text)
    if opt == None:
        await message.answer("Пожалуйста, выберите вариант, используя клавиатуру ниже.")
        return
    else:
        await save_answer(state, opt.id, message.from_user.id)
        if (await incr_question(state)):
            i_q, active_question = await get_cur_question(state)
            await message.answer("{}) {}".format(i_q + 1, active_question.question), \
                            reply_markup=active_question.keyboard)
        else:
            await SurveyState.final.set()
            await message.answer("Вопросы закончились \U0001F37A\U0001F449\U0001F44C", 
                                    reply_markup=final_keyboard)


async def end_survey(message: types.Message, state: FSMContext):
    answers = list()
    async with state.proxy() as data:
        answers = data["answers"]
    await record_answers_db(answers)
    await state.finish()
    await message.answer("Спасибо, что поучаствовали в опросе!", \
                            reply_markup=types.ReplyKeyboardRemove())


async def cmd_previous(message: types.Message, state: FSMContext):
    await decr_question(state)
    i_q, active_question = await get_cur_question(state)
    await message.answer("{}) {}".format(i_q + 1, active_question.question), \
                            reply_markup=active_question.keyboard)


async def cmd_interrupt_survey(message: types.Message, state: FSMContext):
    if await state.get_state() is not None:
        await state.finish()
    await message.answer("Спасибо, что поучаствовали в опросе!")


async def cmd_help(message: types.Message):
    await message.answer("Введите /start чтобы начать опрос")


def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state=None)
    dp.register_message_handler(cmd_help, state=None)
    dp.register_message_handler(cmd_previous, commands="previous", state=SurveyState)
    dp.register_message_handler(cmd_interrupt_survey, commands="interrupt", state="*")
    dp.register_message_handler(cmd_previous, Text(equals="Предыдущий вопрос"), state="*")
    dp.register_message_handler(end_survey, Text(equals="Закончить опрос"), state=SurveyState.final)
    dp.register_message_handler(get_answer, state=SurveyState.waiting_for_answer)
