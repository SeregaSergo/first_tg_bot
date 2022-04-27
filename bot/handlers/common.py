from aiogram import Dispatcher, types
from telebot import TeleBot
from filters import isNotPrivate, isNotMember


# Фразы для общния с клиентом/админом
class Phrases():
    NO_QUESTION = "У нас не осталось к вам вопросов!"
    END_OF_QUESTIONS = "Вопросы закончились \U0001F37A\U0001F449\U0001F44C"
    INCORRECT_ANSWER = "Пожалуйста, выберите вариант, используя клавиатуру ниже."
    END_OF_SURVEY = "Спасибо, что поучаствовали в опросе!"
    ONE_MORE_SURVEY = "Для вас есть еще один новый опрос, нажмите /start, чтобы начать."
    START_HELP = "Введите /start чтобы начать опрос"
    START_HELP_ADM = "/start - начать опрос.\n/list_reports - вывести список завершенных опросов.\n/report_current - получить промежуточный отчет по текущему опросу."
    NO_ACCESS = "Вы не являетесь членом закрытой группы компании! Обратитесь к администраторам группы."
    WELCOME = "У нас есть к вам {} вопрос{}!"


phrases = Phrases()


async def no_access(message: types.Message):
    await message.answer(phrases.NO_ACCESS)
    return


async def do_nothing(message: types.Message):
    return


def register_common_handlers(dp: Dispatcher, group_id: int, telebot: TeleBot):
    dp.register_message_handler(do_nothing, isNotPrivate())
    dp.register_message_handler(no_access, isNotMember(group_id, telebot))