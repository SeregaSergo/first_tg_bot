import sqlite3
from typing import List, Tuple
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, User
from aiogram.dispatcher import FSMContext


global survey_dict
survey_dict = dict()

class Option:

    def __init__(self, id, option):
    
        self.id: int = id   # ID ответа
        self.option: str = str(option)   # Текст ответа
        self.button: KeyboardButton = KeyboardButton(option)

    def __str__(self):
        return f"({self.id}){self.option}"


class Question():
    
    def __init__(self, id, question, options, rw, first = False):
        self.id: int = id   # ID вопроса
        self.question: str = question   # Текст вопроса
        self.options: List[Option] = [*options]    # "Распакованное" содержимое массива options в массив self.options
        self.keyboard = ReplyKeyboardMarkup(resize_keyboard=True, \
                                            row_width=rw)

        for opt in options:
            self.keyboard.insert(opt.button)
        if not first:
            self.keyboard.add(KeyboardButton("Предыдущий вопрос"))
    
    def __str__(self):
        return f"{self.id}) {self.question}\n{self.options}\n"

    def check_option(self, answer):
        for option in self.options:
            if answer == option.option:
                return option
        return None


class SurveyGenerator:
    
    def __init__(self, id):
        self.id: int = id   # ID опроса
        self.questions = list()
        self.temp_options = list()

    def add_question(self, id, question, type):
        rw = 1 if type == "choosing" else 5
        first = len(self.questions) == 0
        self.questions.append(Question(id, question, self.temp_options, \
                                        rw, first))
        self.temp_options.clear()

    def add_option(self, id, text):
        self.temp_options.append(Option(id, text))
    
    def save_in_dict(self, dictionary):
        dictionary[self.id] = self.questions


class DBCommands:

    GET_SURV_OPTIONS = "SELECT id_survey, Questions.id, Options.id, \
                        question, type, option FROM Questions \
                        INNER JOIN Options ON Questions.id = Options.id_question \
                        INNER JOIN QuestionTypes ON Questions.id_type = QuestionTypes.id \
                        WHERE id_survey == ?"
    
    GET_SURVEY_BY_ID = "SELECT * FROM Surveys WHERE id_survey == ?"

    GET_LAST_SURVEY = "SELECT * FROM Surveys ORDER BY id DESC LIMIT 1"

    GET_PREV_SURVEY = "SELECT * FROM Surveys ORDER BY id DESC LIMIT 2"

    CHECK_IF_USER_ANSWERED = "SELECT EXISTS (SELECT 1 FROM Questions \
                              INNER JOIN Options ON Questions.id = Options.id_question \
                              INNER JOIN Answers ON Options.id = Answers.id_option \
                              WHERE id_user == ? AND id_survey == ? LIMIT 1)"

    SAVE_USER_ANSWERS = "INSERT INTO Answers (id_option, id_user, datetime) VALUES(?, ?, ?)"
    
    CREATE_REPORT_A = "SELECT id_user, question, option, datetime FROM Questions \
                       INNER JOIN Options ON Questions.id = Options.id_question \
                       INNER JOIN Answers ON Options.id = Answers.id_option \
                       WHERE id_survey == ?"

    CREATE_REPORT_S = "SELECT question, option FROM Questions \
                       INNER JOIN Options ON Questions.id = Options.id_question \
                       INNER JOIN QuestionTypes ON Questions.id_type = QuestionTypes.id \
                       WHERE id_survey == ?"


    def __init__(self, path_db, path_init_cmd):
        self.conn = sqlite3.connect(path_db)
        self.cursor = self.conn.cursor()

        with open(path_init_cmd, "r") as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.conn.commit()
    

    async def add_survey_to_active(self, id: int):
        rows = self.cursor.execute(self.GET_SURV_OPTIONS, (id,)).fetchall()
        generator = SurveyGenerator(id)
        temp_q_id = rows[0][1]
        for i in range(0, len(rows)):
            if rows[i][1] != temp_q_id:     # if option relates to next question:
                generator.add_question(temp_q_id, rows[i-1][3], rows[i-1][4])
                temp_q_id = rows[i][1]
            generator.add_option(rows[i][2], rows[i][5])
        generator.add_question(temp_q_id, rows[i-1][3], rows[i-1][4])
        generator.save_in_dict(survey_dict)


    def get_last_survey_info(self):
        try:
            survey_info = self.cursor.execute(self.GET_LAST_SURVEY).fetchone()
        except(TypeError) as e:
            return None
        return survey_info


    async def get_prev_survey_info(self):
        try:
            result = self.cursor.execute(self.GET_PREV_SURVEY).fetchall()
            if (len(result) < 2):
                return None
            survey_info = result[0]
        except(TypeError) as e:
            return None
        return survey_info


    async def get_survey(self, user_id: int, state: FSMContext):
        id_survey = self.get_last_survey_info()[0]
        if id_survey is None:
            return 0
        if survey_dict.get(id_survey) is None:
            await self.add_survey_to_active(id_survey)

        if self.cursor.execute(self.CHECK_IF_USER_ANSWERED, (user_id, id_survey)).fetchone()[0]:
            return 0

        async with state.proxy() as data:
            data["id_survey"] = id_survey
            data["cur_question"] = 0
            data["num_q"] = len(survey_dict[id_survey])
            data["num_surveys"] = len(survey_dict)
            data["answers"] = list()
        return len(survey_dict[id_survey])


    async def record_answers_db(self, answers: List):
        self.cursor.executemany(self.SAVE_USER_ANSWERS, (answers))
        self.conn.commit()
    

    async def create_report(self, id=None) -> Tuple:
        if id is None:
            info_survey = self.get_last_survey_info()
            if info_survey is None:
                return None
            id = info_survey[0]
        else:
            info_survey = self.cursor.execute(self.GET_SURVEY_BY_ID, (id,)).fetchone()
        survey_table = self.cursor.execute(self.CREATE_REPORT_S, (id,)).fetchall()
        answers_table = self.cursor.execute(self.CREATE_REPORT_A, (id,)).fetchall()


db = DBCommands("../db/database.db", "../db/create_database.sql")