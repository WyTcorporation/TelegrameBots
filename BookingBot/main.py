import asyncio
import logging
import sys

import psycopg_pool
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import BotCommand, BotCommandScopeDefault
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from BookingBot.core.handlers.AdminOperations import answerReserve
from BookingBot.core.handlers.Orders import order, preCheckoutQuery, buyComplete
from BookingBot.core.handlers.Steps import getName, getDate, getTime, getService, getAddService, handleAddService, \
    application, checkPhone, addServiceChancel, clearCart, getHelp
from BookingBot.core.middleware.DBMiddleware import DbSession
from BookingBot.core.other.DBSelfUpdate import DBEntry
from BookingBot.core.other.UserStates import UserStates
from BookingBot.core.Settings import settings

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
    dp.message.middleware(
        DbSession(await dbConnection(settings.db.user, settings.db.password, settings.db.db, settings.db.host)))
    dp.callback_query.middleware(
        DbSession(await dbConnection(settings.db.user, settings.db.password, settings.db.db, settings.db.host)))

    dp.startup.register(botStart)
    dp.shutdown.register(botShutDown)

    dp.message.register(buyComplete, F.content_type.in_('successful_payment'))
    dp.pre_checkout_query.register(preCheckoutQuery)
    dp.callback_query.register(order, F.data == 'order')
    dp.callback_query.register(clearCart, F.data == 'clearCart')
    dp.callback_query.register(addServiceChancel, F.data == 'addServiceChancel')
    dp.callback_query.register(answerReserve, F.data.regexp('adminConfirm') | F.data.regexp('adminCancel'))
    dp.callback_query.register(application, F.data == 'application')
    dp.message.register(checkPhone, UserStates.stateGetPhone)
    dp.callback_query.register(handleAddService, UserStates.stateAddService)
    dp.callback_query.register(getAddService, UserStates.stateService)
    dp.callback_query.register(getService, UserStates.stateTime)
    dp.callback_query.register(getTime, UserStates.stateDate)
    dp.message.register(getDate, UserStates.stateFullName)
    dp.message.register(getName, Command(commands=['start']))
    dp.message.register(getHelp, Command(commands=['help']))
    # pip install apscheduler     # Щоб виставити оновлення у конкретний час
    scheduler = AsyncIOScheduler(timezone='Europe/Kiev')
    scheduler.add_job(DBEntry, 'cron', hour=1, minute=00, start_date='2023-09-08 19:00:00')
    scheduler.start()
    # await DBEntry()
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
