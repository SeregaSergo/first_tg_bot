import configparser
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str
    admin_id: int
    group_id: int


@dataclass
class Config:
    def __init__(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        self.tg_bot=TgBot(
            token=config["tg_bot"]["token"],
            admin_id=int(config["tg_bot"]["admin_id"]),
            group_id=int(config["tg_bot"]["group_id"])
        )