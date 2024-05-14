from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandObject, CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from HouseBot.core.Keyboards.TextButtonsKb import getButtons
from HouseBot.core.other.Request import Request
from HouseBot.core.other.States import States


async def getName(message: Message, state: FSMContext, request: Request):
    await message.answer(
        'Привіт, Я помічник Кеша. Чим я можу Вам допомогти?',
        reply_markup=await getButtons())
    await state.set_state(States.stateNumber)
    await request.dbAddUser(message.from_user.id,
                            message.from_user.first_name,
                            message.from_user.last_name,
                            message.from_user.last_name,
                            message.from_user.username)


async def getHelp(message: Message, request: Request):
    await message.answer(
        'Привіт, звертайтесь по почті wyt.corp2@gmail.com або @wytcorp',
        reply_markup=None)
    await request.dbAddUser(message.from_user.id,
                            message.from_user.first_name,
                            message.from_user.last_name,
                            message.from_user.last_name,
                            message.from_user.username)


async def getNumber(message: Message, state: FSMContext, request: Request):
    try:
        if 'Охорона' == message.text:
            text = f'Охорона (1кпп): +380673542917\n' \
                   f'Охорона (2кпп): +380675362680'
            await message.answer(f'{text}')
        elif 'Комунальні послуги' == message.text:
            text = f'ЖЕК: +380681164612\n' \
                   f'пн, вт, чт: 9 - 18\n' \
                   f'ср, пт: 9 - 13\n' \
                   f'Бухгалтер: +380689740370\n' \
                   f'Диспетчер: +380681164615\n\n' \
                   f'Домофони: +380504489977\n' \
                   f'Котли: +380983331733\n' \
                   f'Ліфти: 0800501901\n' \
                   f'Газ: <a href="https://104.ua/ua">104.ua</a> / <a href="https://my.gas.ua/login">my.gas.ua</a>\n' \
                   f'Вода: <a href="https://ok.vodasofia.kiev.ua">ok.vodasofia.kiev.ua</a>\n' \
                   f'Електроенергія: <a href="https://ok.koec.com.ua">ok.koec.com.ua</a>\n' \
                   f'ДТЕК: <a href="https://my.dtek-krem.com.ua">my.dtek-krem.com.ua</a>\n'
            await message.answer(f'{text}')
        elif 'Нова + Укр пошта' == message.text:
            text = f'Нова Пошта\n' \
                   f'Поштомат Гурман, Головний, 25887\n' \
                   f'Поштомат Гурман, Алея, 35550\n' \
                   f'Поштомат вул. Зелена, 10, 36295\n' \
                   f'Нова пошта, №7, вул.Шалімова, 67\n\n' \
                   f'Укрпошта\n' \
                   f'08147, вул.Дорошенка, 15\n' \
                   f'08176, вул.Абрикосова, 1г\n'
            await message.answer(f'{text}')
        elif 'Амбулаторії' == message.text:
            text = f'Амбулаторія\n' \
                   f'вул. Соборна, 53б\n' \
                   f'+380673143244\n\n' \
                   f'Невідкладна допомога: м. Боярка\n' \
                   f'+380459868103\n' \
                   f'+380456310051\n'
            await message.answer(f'{text}')
        elif 'Інтернет + Телебачення' == message.text:
            text = f'Інтернет <a href="https://my.ukr-link.net">my.ukr-link.net</a>\n' \
                   f'Telegram: @internet_provider\n' \
                   f'+380672200695\n' \
                   f'+380931701181\n' \
                   f'+380504100445\n' \
                   f'+380443640089\n\n' \
                   f'Телебачення "Максимум"\n' \
                   f'+380980000869\n' \
                   f'+380930000869\n' \
                   f'+380990000869\n' \
                   f'+380443740451\n'
            await message.answer(f'{text}')
        elif 'Маршрутки' == message.text:
            text = f'Маршрутки\n' \
                   f'742: Академмістечко - Боярка.\n' \
                   f'796: Академмістечко - Боярка.\n' \
                   f'769: Нивки - Горбовичи.\n' \
                   f'824: Нивки - Княжичи.\n' \
                   f'374: Виставковий центр - Білогородка.\n' \
                   f'744: Петропавлівська Борщагівка - ж/м Західний.\n' \
                   f'304Д: Львівський маєток - Академмістечко.\n'
            await message.answer(f'{text}')
        elif 'Світло є?(в розробці)' == message.text:
            text = f'Світло є?(в розробці)'
            await message.answer(f'{text}')
    except TelegramBadRequest as e:
        print(e)
