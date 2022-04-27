python3 -m pip install --upgrade pip
pip install -r requirements.txt
python3 %~dp0/upload_survey/questions.py survey2.xlsx
python3 bot.py