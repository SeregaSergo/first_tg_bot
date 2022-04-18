import sqlite3
import copy
from typing import List
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from questions.questions import survey_dict


conn = sqlite3.connect("db_dir/database.db")
cursor = conn.cursor()

class Option:

    def __init__(self, id, option):
    
        self.id: int = id   # ID ответа
        self.option: str = str(option)   # Текст ответа
        self.button: KeyboardButton = KeyboardButton(option)

    def __str__(self):
        return f"({self.id}){self.option}"


class Question:
    
    def __init__(self, id, question, type_q, first = False, options = list()):
        self.id: int = id   # ID вопроса
        self.question: str = question   # Текст вопроса
        self.type: str = type_q
        self.options: List[Option] = [*options]    # "Распакованное" содержимое массива options в массив self.options
        self.keyboard = ReplyKeyboardMarkup(resize_keyboard=True, \
                                            row_width=5 if type_q == "eval" else 1)
        self.first = first

        for opt in options:
            if type_q == "eval":
                self.keyboard.insert(opt.button)
            else:
                self.keyboard.add(opt.button)
        if not first and len(options) != 0:
            self.keyboard.add(KeyboardButton("Предыдущий вопрос"))

    def __str__(self):
        options = str()
        for opt in self.options:
            options += str(opt) + "  "
        return f"{self.id}){self.question}\n{options}\n"

    def add_option(self, opt: Option):
        self.options.append(opt)
        if self.type == "eval":
            self.keyboard.insert(opt.button)
        else:
            self.keyboard.add(opt.button)

    def check_option(self, answer):
        for option in self.options:
            if answer == option.option:
                return option
        return None
    
    def check_id_option(self, id_o):
        for option in self.options:
            if id_o == option.id:
                return True
        return False


class Survey:
    
    def __init__(self, id, date, questions):
        self.id: int = id   # ID опроса
        self.date: str = date   # Дата добавления опросника
        self.questions: List[Question] = [*questions]    # "Распакованное" содержимое массива questions в массив self.questions

    def __str__(self):
        questions = str()
        for q in self.questions:
            questions += str(q) + "\n*******\n"
        return f"SURVEY #{self.id}\n{questions}\n"


async def add_survey_to_active(id: int):
    temp = cursor.execute("SELECT id_survey, Questions.id_question, Options.id_option, question, type, option \
                                FROM Questions \
                                INNER JOIN Options \
                                ON Questions.id_question = Options.id_question \
                                INNER JOIN QuestionTypes \
                                ON Questions.id_type = QuestionTypes.id_type \
                                WHERE id_survey == ?", (id,)).fetchall()
    temp_q = None
    for opt in temp:
        if temp_q is None:
            survey_dict[id] = list()
            temp_q = Question(opt[1], opt[3], opt[4], True)
        elif temp_q.id != opt[1]:
            if not temp_q.first:
                temp_q.keyboard.add(KeyboardButton("Предыдущий вопрос"))
            survey_dict[id].append(temp_q)
            temp_q = Question(opt[1], opt[3], opt[4])
        temp_q.add_option(Option(opt[2], opt[5]))
    temp_q.keyboard.add(KeyboardButton("Предыдущий вопрос"))
    survey_dict[id].append(temp_q)


async def get_last_survey():
    id_survey, date = cursor.execute("SELECT * FROM Surveys ORDER BY id_survey DESC LIMIT 1").fetchone()
    if id_survey is None:
        return None
    if survey_dict.get(id_survey) is None:
        await add_survey_to_active(id_survey)
    return id_survey


async def get_survey(user_id: int, state: FSMContext):
    id_survey = await get_last_survey()
    if id_survey is None:
        return 0
    
    answered_survey = cursor.execute("SELECT id_survey \
                                        FROM Questions \
                                        INNER JOIN Options \
                                        ON Questions.id_question = Options.id_question \
                                        INNER JOIN Answers \
                                        ON Options.id_option = Answers.id_option \
                                        WHERE id_user == ? AND id_survey == ?", (user_id, id_survey)).fetchall()

    if len(answered_survey) != 0:
            return 0

    async with state.proxy() as data:
        data["id_survey"] = id_survey
        data["cur_question"] = 0
        data["num_q"] = len(survey_dict[id_survey])
        data["answers"] = list()
    return len(survey_dict[id_survey])


async def record_answers_db(answers: List):
    cursor.executemany("INSERT INTO answers (id_option, id_user, datetime) VALUES(?, ?, ?)", (answers))
    conn.commit()
    

# Инициализирует БД
def start_db():
    with open("db_dir/create_database.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()
