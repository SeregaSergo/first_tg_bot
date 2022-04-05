from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from click import command

        
final_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Закончить опрос"),
                                                    KeyboardButton(text="Вернуться")]],
                                    resize_keyboard=True)