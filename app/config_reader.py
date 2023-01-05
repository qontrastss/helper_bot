import configparser
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str
    admin1_id: int
    admin2_id: int
    admin3_id: int


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"],
            admin1_id=int(tg_bot["admin1_id"]),
            admin2_id=int(tg_bot["admin2_id"]),
            admin3_id=int(tg_bot["admin3_id"]),
        )
    )
