from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


async def kbGetService():
    dictServices = {
        'Піксі': 100,
        'Боб': 99,
        'Мілітарі': 98,
        'Гарсон': 97,
        'Гранж': 96,
        'Автора': 95,
        'Голлівуд': 94,
        'Італійка': 93,
        'Асиметрія': 92,
        'Лісенка': 91,
        'Шеггі': 90,
        'Вовчиця': 80
    }

    serviceList: List[InlineKeyboardButton] = []
    buttons = []
    for k, v in dictServices.items():
        if len(serviceList) == 3:  # 3 кнопки в ряд
            buttons.append(serviceList)
            serviceList = []

        button = InlineKeyboardButton(
            text=f'{k}-{v}',
            callback_data=f'reserveTime={k}|{v}'
        )
        serviceList.append(button)

    buttons.append(serviceList)
    # print(buttons)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def kbGetAddService():
    dictServices = {
        'Манікюр': 100,
        'Педикюр': 10,
        'Вії': 50
    }

    serviceList: List[InlineKeyboardButton] = []
    buttons = []
    for k, v in dictServices.items():
        if len(serviceList) == 3:  # 3 кнопки в ряд
            buttons.append(serviceList)
            serviceList = []

        button = InlineKeyboardButton(
            text=f'{k}-{v}',
            callback_data=f'reserveTime={k}|{v}'
        )
        serviceList.append(button)

    buttons.append(serviceList)
    buttonCancel = InlineKeyboardButton(
        text=f'Дякую не потрібно',
        callback_data=f'addServiceChancel'
    )
    buttons.append([buttonCancel])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
