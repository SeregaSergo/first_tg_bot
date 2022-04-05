import sqlite3
import types
from typing import List
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import questions.questions as q


conn = sqlite3.connect("db_dir/database.db")
cursor = conn.cursor()

class Option:

    def __init__(self, id, option):
    
        self.id: int = id   # ID ответа
        self.option: str = option   # Текст ответа
        self.button: KeyboardButton = KeyboardButton(option)

    def __str__(self):
        return f"({self.id}){self.option}"


class Question:
    
    def __init__(self, id, question, options):
        self.id: int = id   # ID вопроса
        self.question: str = question   # Текст вопроса
        self.options: List[Option] = [*options]    # "Распакованное" содержимое массива options в массив self.options
        self.keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
        for opt in options:
            self.keyboard.add(opt.button)

    def __str__(self):
        options = str()
        for opt in self.options:
            options += str(opt) + "  "
        return f"{self.id}){self.question}\n{options}\n"

    def check_option(self, answer):
        for option in self.options:
            if answer == option.option:
                return option
        return None


async def count_questions(user_id: int):
    nums = list()
    answered_questions = cursor.execute("SELECT id_question \
                                        FROM answers \
                                        INNER JOIN options \
                                            ON options.id_option = answers.id_option \
                                        WHERE id_user == ?", (user_id,)).fetchall()
    answered_questions = [elem[0] for elem in answered_questions]
    for i in range(len(q.question_list)):
        if q.question_list[i].id not in answered_questions:
            nums.append(i)
    return nums


async def record_answers_db(answers: List):
    cursor.executemany("INSERT INTO answers (id_option, id_user, datetime) VALUES(?, ?, ?)", (answers))
    conn.commit()


def get_question_db(question: str, options: list):
    id_q = cursor.execute("SELECT id_question from questions WHERE question == ?",\
                            (question,)).fetchone()
    opt_list = list()

    if id_q:
        id_q = id_q[0]
        for opt in options:
            id_o = cursor.execute("SELECT id_option from options WHERE option == ? AND id_question == ?",\
                            (opt, id_q)).fetchone()
            if id_o == None:
                cursor.execute("INSERT INTO options (option, id_question) VALUES(?, ?)", (opt, id_q))
                id_o = cursor.lastrowid
            else:
                id_o = id_o[0]
            opt_list.append(Option(id_o, opt))

    else:
        cursor.execute("INSERT INTO questions (question) VALUES(?)", (question,))
        id_q = cursor.lastrowid
        for opt in options:
            cursor.execute("INSERT INTO options (option, id_question) VALUES(?, ?)", (opt, id_q))
            opt_list.append(Option(cursor.lastrowid, opt))

    conn.commit()
    return(Question(id_q, question, opt_list))
    

# Инициализирует БД
def start_db():
    with open("db_dir/create_database.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()
