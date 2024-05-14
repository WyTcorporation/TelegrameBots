import asyncio
import logging
import sys

# import psycopg_pool
import mysql.connector
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommand, BotCommandScopeDefault
from aiogram.utils.markdown import hbold

from modules.handlers.Steps import getName, getHelp, getNumber
from modules.middleware.DBMiddleware import DbSession
from modules.other.Request import Request
from modules.Settings import settings

router = Router()

if sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


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
    return mysql.connector.connect(
        database=database,
        host=host,
        user=user,
        password=password
    )
    # return psycopg_pool.AsyncConnectionPool(
    #     f'host={host} port=3306 dbname={database} user={user} password={password} connect_timeout=10')


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext, request: Request) -> None:
    await getName(message, state, request)
    # await message.answer(f"Start, {hbold(message.from_user.full_name)}!")


@router.message(Command('help'))
async def command_start_handler(message: Message, request: Request) -> None:
    await getHelp(message, request)
    # await message.answer(f"Help, {hbold(message.from_user.full_name)}!")


@router.message()
async def echo_handler(message: types.Message) -> None:
    try:
        # await message.send_copy(chat_id=message.chat.id)
        await getNumber(message)
    except TypeError as e:
        await message.answer(f"Помилка відповіді! - {e}")


async def main() -> None:
    bot = Bot(settings.bots.botToken, parse_mode=ParseMode.HTML)
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)
    dp.startup.register(botStart)
    dp.shutdown.register(botShutDown)
    dp.message.middleware(
        DbSession(await dbConnection(settings.db.user, settings.db.password, settings.db.db, settings.db.host)))
    dp.callback_query.middleware(
        DbSession(await dbConnection(settings.db.user, settings.db.password, settings.db.db, settings.db.host)))

    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f'Error bot - {e}')
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")

# Додаємо на сервак даймонта, щоб він автоматично запускався з сервером
# apt-get install system
# Створюємо папку system та файл з налаштуваннями bot_service
# systemctl daemont-reload ребутнимо
# systemctl enable /bots/NewHouseBot/systemd/bot.service додамо в автозагрузку