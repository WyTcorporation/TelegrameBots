import re

import emoji
from aiogram import Bot
from aiogram.filters import CommandObject, CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import decode_payload
from LightOnOff.core.Keyboards.StepsKb import kbGetAreas, kbGetCities, refreshButtons
from LightOnOff.core.Keyboards.TextButtonsKb import getButtonFullName
from LightOnOff.core.other.Request import Request
from LightOnOff.core.other.States import States


async def getName(message: Message, command: CommandObject, state: FSMContext, request: Request):
    print(message.from_user.language_code)
    print(command.args)
    print(message.get_url())
    # payload = decode_payload(args)
    # print(payload)
    await message.answer(
        'Привіт, Я помічник компанії Електро Україна. В нас можна дізнатися чи є світло! Як я можу до Вас звертатися?',
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


async def getAreas(message: Message, state: FSMContext, request: Request):
    await message.answer(f'Приємно познайомитися {message.text}, виберіть вашу область: ',
                         reply_markup=await kbGetAreas(request))
    await state.update_data(fullName=message.text)
    await state.set_state(States.stateArea)


async def getCity(call: CallbackQuery, state: FSMContext):
    dateArea = call.data.split('=')[1]
    await call.message.edit_text(f'Тепер будь-ласка введіть ваше місто \r\n (це демо, тому обласний центр):')
    await state.update_data(area=dateArea)
    await state.set_state(States.stateCityText)


async def searchCity(message: Message, state: FSMContext, request: Request):
    city = message.text
    data = await state.get_data()
    area = data['area']
    areaId = area.split('|')[0]
    db = await request.dbGetCity(areaId, city)
    if len(db) > 0:
        await message.answer(f'Виберіть місто з нашого списку для точності: ',
                             reply_markup=await kbGetCities(request, db))
        await state.update_data(cityText=city)
        await state.set_state(States.stateCity)
    else:
        await message.answer(f'Вибачте такого міста не знайдено, спробуйте ще раз!')


async def getStreet(call: CallbackQuery, state: FSMContext):
    dateCity = call.data.split('=')[1]
    await call.message.edit_text(
        # f'Дякую, останній шаг. Введіть вулицю та будинок через кому \r\n (Наприклад: Хрещатик, 22):' + emoji.emojize(":brain:"))
        f'Дякую, останній шаг. Введіть вулицю та будинок через кому \r\n (Наприклад: Хрещатик, 22):')
    await state.update_data(city=dateCity)
    await state.set_state(States.stateStatus)


async def results(message: Message, state: FSMContext, request: Request):
    street = message.text
    # Тут код пошуку по вулицях і статусу є світло чи ні
    # За допомогою IP-адреси бот перевіряє, чи підключений роутер до мережі.
    # Якщо ні, значить електрики у цьому приміщенні немає.
    # Сервіс працюватиме за наявності статичного або динамічного IP
    data = await state.get_data()
    area = data['area'].split('|')[1]
    city = data['city'].split('|')[1]
    await message.answer(
        f'За адресою {area} - {city} - {street}\r\n\r\nНа данний момент світло є, щаслива людина!\r\n\r\n🇺🇦 Все буде Україна!',
        reply_markup=await refreshButtons())
    await state.update_data(street=street)


async def update(call: CallbackQuery, state: FSMContext):
    # Тут код пошуку по вулицях і статусу є світло чи ні
    # За допомогою IP-адреси бот перевіряє, чи підключений роутер до мережі.
    # Якщо ні, значить електрики у цьому приміщенні немає.
    # Сервіс працюватиме за наявності статичного або динамічного IP
    typeAnswer = call.data.split('=')[1]
    print(typeAnswer)
    data = await state.get_data()
    area = data['area'].split('|')[1]
    city = data['city'].split('|')[1]
    street = data['street']

    if typeAnswer != 0:
        text = f'Cвітла немає, нажаль!'
        number = 0
    else:
        text = f'Cвітло є, щаслива людина!'
        number = 1
    await call.message.edit_text('Оновлення', reply_markup=None)
    await call.message.edit_text(f'За адресою\r\n{area} - {city} - {street}\r\n\r\n{text}\r\n\r\n🇺🇦 Все буде Україна!',
                                 reply_markup=await refreshButtons(number))


async def restart(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await call.message.edit_text(f'Щоб почати заново напишіть /start або використайте меню', reply_markup=None)
