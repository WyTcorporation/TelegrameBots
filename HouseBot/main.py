import asyncio
import logging
import sys

import psycopg_pool
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommandScopeDefault, BotCommand

from HouseBot.core.handlers.Steps import getName, getHelp, getNumber
from HouseBot.core.other.States import States
from HouseBot.core.middleware.DBMiddleware import DbSession
from HouseBot.core.Settings import settings

if sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logger = logging.getLogger(__name__)


async def commands(bot: Bot):
    command = [
        BotCommand(
            command='start',
            description='Запустити бота!'
        ),
        BotCommand(
            command='help',
            description='Допомога'
        )
    ]
    await bot.set_my_commands(command, BotCommandScopeDefault())


async def botStart(bot: Bot):
    await commands(bot)
    await bot.send_message(chat_id=settings.bots.adminId, text='Бот запущений!')


async def botShutDown(bot: Bot):
    await bot.send_message(chat_id=settings.bots.adminId, text='Бот вимкнено!')


async def dbConnection(user, password, database, host):
    return psycopg_pool.AsyncConnectionPool(
        f'host={host} port=5432 dbname={database} user={user} password={password} connect_timeout=10')


async def runBot():
    logging.basicConfig(
        level=logging.INFO
    )
    logger.info('Бот стартував!')

    bot = Bot(settings.bots.botToken, parse_mode='HTML')
    dp = Dispatcher()
    dp.startup.register(botStart)
    dp.shutdown.register(botShutDown)
    dp.message.middleware(
        DbSession(await dbConnection(settings.db.user, settings.db.password, settings.db.db, settings.db.host)))
    dp.callback_query.middleware(
        DbSession(await dbConnection(settings.db.user, settings.db.password, settings.db.db, settings.db.host)))
    dp.message.register(getNumber, States.stateNumber)
    dp.message.register(getName, Command(commands=['start']))
    dp.message.register(getHelp, Command(commands=['help']))

    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f'Error bot - {e}')
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(runBot())
    except(KeyboardInterrupt, SystemExit, SystemError):
        print('Error run')