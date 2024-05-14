import asyncio
import logging
import sys

import psycopg_pool
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import BotCommandScopeDefault, BotCommand

from EnergyBot.core.handlers.Steps import getName, getHelp, getInformation, getNumber, allInfo, tariff, tariffs, \
    tariffCounters, tariffTech, tariffOnOff, contact, contacts, clearing, adding, addIndication, clearingTrue, \
    clearingFalse, back, emergencyShutdowns, communication, noElectricity
from EnergyBot.core.other.States import States
from EnergyBot.core.middleware.DBMiddleware import DbSession
from EnergyBot.core.Settings import settings

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
    # await bot.send_message('','Доброго дня! Щоб почати наберіть /start або скористайтесь меню.')
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
    dp.message.register(getName, Command(commands=['start']))
    dp.message.register(getHelp, Command(commands=['help']))


    dp.callback_query.register(communication, F.data == 'communication')
    dp.callback_query.register(noElectricity, F.data == 'noElectricity')
    dp.callback_query.register(emergencyShutdowns, F.data == 'emergencyShutdowns')
    dp.callback_query.register(contacts, F.data == 'contacts')
    dp.callback_query.register(back, F.data == 'back')
    dp.callback_query.register(tariffCounters, F.data == 'tariffCounters')
    dp.callback_query.register(tariffTech, F.data == 'tariffTech')
    dp.callback_query.register(tariffOnOff, F.data == 'tariffOnOff')
    dp.callback_query.register(tariffs, F.data == 'tariffs')
    dp.callback_query.register(tariff, F.data == 'tariff')
    dp.callback_query.register(clearingFalse, F.data == 'clearingFalse')
    dp.callback_query.register(clearingTrue, F.data == 'clearingTrue')
    dp.message.register(addIndication, States.stateIndication)
    dp.callback_query.register(clearing, F.data == 'clearing')
    dp.callback_query.register(adding, F.data == 'adding')
    dp.callback_query.register(allInfo, F.data == 'allInfo')
    dp.message.register(getNumber, States.stateNumber)
    dp.message.register(getInformation, States.stateFullName)

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


# З точки зору Юзер інтерфейсу - статус надання послуги за адресою (типу є світло чи відсутнє)
# Якщо відсутнє, то причину і орієнтовний час відновлення ее (але щоб чесно).
# Також було би добре інформувати про планові відключення.

# І саме головне - кому нахрен належить щитова і контактний номер для комунікації.

# З точки зору вигоди бізнесу (це для ДТЕК) - можна надавати інфо по тарифу, заборгованості, споживанню.
# Я думав 6 місяців, і оплачений і не оплачений статус і дата нарахування І цифри скільки нараховано і показання поточного лічільника
# І ще - номер телефону гарячої лінії саме для мого адресу.
# Також можна закинути форму звернення через бот
# Ну і якщо гулять на всі, то і оплату через бот)

