import copy
from db_dir.dbworker import get_question_db


def parse_file(file):
    temp_list_questions = []
    with open(file) as r:
        key = str()
        temp = []
        for line in r:
            n = line.split('\n')[0]
            if n!= '':
                if n[-1] == '?':
                    if len(key) != 0:
                        temp_list_questions.append((key, copy.deepcopy(temp)))
                    key = n
                    temp.clear()
                else:
                    temp.append(n)
        temp_list_questions.append((key, copy.deepcopy(temp)))
    return (temp_list_questions)


def initialize(): 
    global question_list
    question_list = list()

    temp_list = parse_file('questions/questions.txt')
    for question in temp_list:
        question_list.append(get_question_db(question[0], question[1]))
