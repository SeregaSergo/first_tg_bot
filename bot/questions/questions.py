import copy

global survey_dict
survey_dict = dict()

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
