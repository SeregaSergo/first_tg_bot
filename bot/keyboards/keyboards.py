from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

        
final_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Закончить опрос"),
                                                    KeyboardButton(text="Предыдущий вопрос")]],
                                    resize_keyboard=True)