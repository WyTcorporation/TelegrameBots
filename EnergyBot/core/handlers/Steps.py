import random
import re
import time
import base64

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from EnergyBot.core.Keyboards.StepsKb import kbGetStart, infoButtons, contractButtons, tariffButtons, \
    clearingButtons
from EnergyBot.core.Keyboards.TextButtonsKb import getButtonFullName
from EnergyBot.core.other.Request import Request
from EnergyBot.core.other.States import States


def deeplink(botName, arg):
    return f'https://t.me/{botName}?start={arg.encode("utf-8")}'


async def getName(message: Message, state: FSMContext, request: Request):
    # print(message.from_user.language_code)
    await message.answer(
        'Привіт, Я помічник компанії Електро Україна.\r\n'
        'В нас можна дізнатися довідкову інформацію, ваші показники та платежі!\r\n'
        'Як я можу до Вас звертатися?',
        reply_markup=await getButtonFullName(message.from_user.full_name))
    await state.set_state(States.stateFullName)
    await request.dbAddUser(message.from_user.id,
                            message.from_user.first_name,
                            message.from_user.last_name,
                            message.from_user.last_name,
                            message.from_user.username)


async def getHelp(message: Message, state: FSMContext, request: Request):
    await message.answer(
        'Привіт, звертайтесь по почті wild.savedo@gmail.com або @wytcorp',
        reply_markup=None)
    await request.dbAddUser(message.from_user.id,
                            message.from_user.first_name,
                            message.from_user.last_name,
                            message.from_user.last_name,
                            message.from_user.username)


async def getInformation(message: Message, state: FSMContext, request: Request):
    await state.update_data(fullName=message.text)
    await state.set_state(States.stateNumber)
    await message.answer(f'Приємно познайомитися {message.text}, оберіть що Вас цікавить: ',
                         reply_markup=await kbGetStart())


async def getNumber(message: Message, state: FSMContext, request: Request):
    data = await state.get_data()
    if 'contract' in data.keys():
        if 'Перевірити показники' == message.text:
            await message.answer(f'Виберіть яка саме інформація вам потрібна :',
                                 reply_markup=await contractButtons())
        else:
            await message.answer(f'Виберіть послугу :', reply_markup=await infoButtons())
    else:
        if 'Перевірити показники' == message.text:
            await message.answer(f'Будь-ласка введіть номер договору :\n (тест 1111111111)')
        elif 'Інформація' == message.text:
            await message.answer(f'Виберіть послугу :', reply_markup=await infoButtons())
        elif '1111111111' == message.text:
            await message.answer(f'Дякую за інформацію! Виберіть яка саме інформація вам потрібна :',
                                 reply_markup=await contractButtons())
            await state.update_data(contract=message.text)
        else:
            await message.answer(f'<b>Помилка в номері договору!</b>\r\nПовторіть спробу!')


async def allInfo(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    x = 6
    now = time.localtime()
    days = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:3] for n in range(x)]
    contract = data['contract']
    address = f'(вул. Калинова, буд. 22, кв. 54)'
    text = f'Показання\n' \
           f'Номер договору : {contract}\n' \
           f'{address} :\n' \
           f'Дата - Показання - Оплата :\n'
    for day in days:
        number = round(random.uniform(10000, 100000), 1)
        buy = 'Сплачено' if number < 50000 else 'Не сплачено'
        text += f'0{day[2]}.{day[1]}.{day[0]} - {number} - {buy}\n'
    text += f'\n\nЗалишок до сплати : 0.0 грн'
    text += f'\nПереплата : 59.60 грн'
    await call.message.edit_text(text, reply_markup=await contractButtons())


async def adding(call: CallbackQuery, state: FSMContext):
    text = f'Введіть показники в такому форматі (11111.5)'
    await call.message.edit_text(text, reply_markup=None)
    await state.set_state(States.stateIndication)


async def addIndication(message: Message, state: FSMContext, request: Request):
    if 'Перевірити показники' == message.text:
        await message.answer(f'Виберіть яка саме інформація вам потрібна :',
                             reply_markup=await contractButtons())
    elif 'Інформація' == message.text:
        await message.answer(f'Виберіть послугу :', reply_markup=await infoButtons())
    else:
        try:
            indication = float(message.text)
            if len(message.text) - 1 == 6:
                await state.update_data(indication=indication)
                text = f'Дякую за показники: {message.text}, може Вас ще щось цікавить?'
            else:
                text = f'Щось не так, спробуйте ще раз.'
        except ValueError as e:
            text = f'Щось не так, спробуйте ще раз.'

        await message.answer(text,
                             reply_markup=await contractButtons())


async def clearing(call: CallbackQuery, state: FSMContext):
    text = f'Ви впевнені?'
    await call.message.edit_text(text, reply_markup=await clearingButtons())


async def clearingTrue(call: CallbackQuery, state: FSMContext):
    text = f'Данні були видалені! Для продовження напишіть /start або використовуйте меню'
    await state.clear()
    await call.message.answer(text, reply_markup=None)


async def clearingFalse(call: CallbackQuery, state: FSMContext):
    text = f'Виберіть яка саме інформація вам потрібна :'
    await call.message.edit_text(text,
                                 reply_markup=await contractButtons())


async def tariff(call: CallbackQuery, state: FSMContext):
    text = f'Виберіть які тарифи Вас цікавлять : '
    await call.message.edit_text(text, reply_markup=await tariffButtons())


async def tariffs(call: CallbackQuery, state: FSMContext):
    text = f'з 01 червня 2023 року по 30 червня 2023 року:\n' \
           f'для I класу напруги - 142,91 грн/МВт∙год,без ПДВ\n' \
           f'для II класу напруги - 587,12 грн/МВт∙год,без ПДВ\n'
    text += f'\n' \
            f'з 01 липня 2023 року по 31 грудня 2023 року:\n' \
            f'для I класу напруги - 181,60 грн/МВт∙год,без ПДВ\n' \
            f'для II класу напруги - 733,70 грн/МВт∙год,без ПДВ\n' \
            f'\n' \
            f'<a href="https://www.dtek-kem.com.ua/ua/services-tariffs">Потробиці</a>\n' \
            f'\n'
    try:
        await call.message.edit_text(text, reply_markup=await tariffButtons())
    except TelegramBadRequest as e:
        print(e)


async def tariffOnOff(call: CallbackQuery, state: FSMContext):
    text = f'Підключення на опорі (ПЛ 0,22 кВ/0,38 кВ) (однофазний ввід/трифазний ввід) за ініціативою замовника : 2081,15 (грн) з ПДВ\n\n' \
           f'Підключення в однофазному/трифазному лічильнику або на комутаційному апараті (0,22 кВ/ 0,38 кВ) за ініціативою замовника : 1409,05 (грн) з ПДВ\n\n' \
           f'\n' \
           f'<a href="https://www.dtek-kem.com.ua/ua/services-tariffs">Потробиці</a>\n' \
           f'\n'
    try:
        await call.message.edit_text(text, reply_markup=await tariffButtons())
    except TelegramBadRequest as e:
        print(e)


async def tariffTech(call: CallbackQuery, state: FSMContext):
    text = f'Позачергова технічна перевірка правильності роботи (перевірка схеми вмикання) однотарифного однофазного (0,22 кВ) засобу обліку за ініціативою замовника : 601,94 (грн) з ПДВ\n\n' \
           f'Позачергова технічна перевірка правильності роботи (перевірка схеми вмикання) однотарифного трифазного (0,38 кВ прямого включення) засобу обліку за ініціативою замовника : 825,29 (грн) з ПДВ\n\n' \
           f'\n' \
           f'<a href="https://www.dtek-kem.com.ua/ua/services-tariffs">Потробиці</a>\n' \
           f'\n'
    try:
        await call.message.edit_text(text, reply_markup=await tariffButtons())
    except TelegramBadRequest as e:
        print(e)


async def tariffCounters(call: CallbackQuery, state: FSMContext):
    text = f'Дистанційна параметризація електронного багатотарифного лічильника електроенергії (за ініціативою замовника)   : 619,49 (грн) з ПДВ\n\n' \
           f'Параметризація електронного багатотарифного лічильника електроенергії за ініціативою замовника : 758,16 (грн) з ПДВ\n\n' \
           f'\n' \
           f'<a href="https://www.dtek-kem.com.ua/ua/services-tariffs">Потробиці</a>\n' \
           f'\n'
    try:
        await call.message.edit_text(text, reply_markup=await tariffButtons())
    except TelegramBadRequest as e:
        print(e)


async def back(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f'Виберіть послугу :', reply_markup=await infoButtons())


async def contacts(call: CallbackQuery, state: FSMContext):
    text = f'Багатоканальний цілодобовий кол-центр:\n' \
           f'+38 (044) 459 07 40\n\n' \
           f'Окрема лінія для юридичних клієнтів:\n' \
           f'+38 (050) 495 70 40\n\n' \
           f'Для мобільних телефонів:\n' \
           f'+38 (067) 495 70 40\n' \
           f'+38 (099) 495 70 40\n' \
           f'+38 (093) 495 70 40\n\n' \
           f'Дзвінки згідно з тарифами мобільних операторів:\n' \
           f'0 800 400 740\n\n' \
           f'\n' \
           f'<a href="https://www.dtek-krem.com.ua/ua/contacts">Потробиці</a>\n' \
           f'\n'
    try:
        await call.message.edit_text(text, reply_markup=await tariffButtons())
    except TelegramBadRequest as e:
        print(e)


async def emergencyShutdowns(call: CallbackQuery, state: FSMContext):
    text = f'Планові і аварійні відключення:\n' \
           f'(Софіївська Борщагівка)\n\n' \
           f'10.08.23 11:00 - 18:00\n' \
           f'18.08.23 14:00 - 18:00\n' \
           f'19.08.23 17:00 - 18:00\n\n' \
           f'<a href="https://www.dtek-kem.com.ua/ua/shutdowns">Потробиці</a>\n' \
           f'\n'
    try:
        await call.message.edit_text(text, reply_markup=await tariffButtons())
    except TelegramBadRequest as e:
        print(e)


async def noElectricity(call: CallbackQuery, state: FSMContext):
    dataText = f'Софіївська Борщагівка'
    link = deeplink('WyTcorpLightOnOffBot',  dataText)
    noYes = 'світло є' if random.choice([True, False]) else 'нає світла'
    text = f'Відсутня електроенергія?\n' \
           f'(Софіївська Борщагівка)\n\n' \
           f'\n' \
           f'Зараз <b>{noYes}</b>, щаслива людина!\n' \
           f'\n' \
           f'Якщо Вам потрібно інформацію по іншим містам\n' \
           f'Скористайтесь нашим ботом по світлу <a href="{link}">@WyTcorpLightOnOffBot</a>\n' \
           f'\n\n' \
           f'<a href="https://www.dtek-kem.com.ua/ua/shutdowns">Подробиці</a>\n' \
           f'\n'
    try:
        await call.message.edit_text(text, reply_markup=await tariffButtons())
    except TelegramBadRequest as e:
        print(e)


async def communication(call: CallbackQuery, state: FSMContext):
    text = f'Контактний номер для комунікації Вашого району:\n' \
           f'(Софіївська Борщагівка)\n\n' \
           f'+38 (067) 495 70 40\n' \
           f'+38 (099) 495 70 40\n' \
           f'09:00 - 18:00\n\n' \
           f'<a href="https://www.dtek-krem.com.ua/ua/contacts">Потробиці</a>\n' \
           f'\n'
    try:
        await call.message.edit_text(text, reply_markup=await tariffButtons())
    except TelegramBadRequest as e:
        print(e)


async def contact(message: Message, state: FSMContext, request: Request):
    await message.answer(f'contact Form: ',
                         reply_markup=await infoButtons())
