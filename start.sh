sudo apt-get install python3
python3 -m pip install --upgrade pip
sudo apt install python3.8-venv
sudo python3 -m venv ~/env
source ~/env/bin/activate
pip install -r requirements.txt
python3 bot.py