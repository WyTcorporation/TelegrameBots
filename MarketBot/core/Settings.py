from dataclasses import dataclass

from environs import Env


@dataclass
class Bots:
    botToken: str
    adminId: str

@dataclass
class Bank:
    bankToken: str

@dataclass
class DB:
    user: str
    password: str
    host: str
    db: str


@dataclass
class Settings:
    bots: Bots
    db: DB
    bank: Bank


# pip install environs

def getStart(path: str):
    env = Env()
    env.read_env(path)
    return Settings(
        bots=Bots(
            botToken=env.str('bot_token'),
            adminId=env.str('admin_id')
        ),
        bank=Bank(
            bankToken=env.str('bank_token')
        ),
        db=DB(
            user=env.str('db_user'),
            password=env.str('db_password'),
            host=env.str('db_host'),
            db=env.str('db_database')
        )
    )


settings = getStart('configs')
# print(settings.bots.bot_token)
