from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List
from LightOnOff.core.other.Request import Request


async def kbGetAreas(request: Request):
    datesList = await request.dbGetAreas()
    # print(datesList)
    dateList: List[InlineKeyboardButton] = []
    buttons = []
    for dl in datesList:
        if len(dateList) == 2:  # 3 кнопки в ряд
            buttons.append(dateList)
            dateList = []

        button = InlineKeyboardButton(
            text=dl[1],
            callback_data=f'areaData={dl[0]}|{dl[1]}'
        )
        dateList.append(button)

    buttons.append(dateList)
    # print(buttons)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def kbGetCities(request: Request, datesList):
    # datesList = await request.dbGetCity(areas_id, city)
    # print(datesList)
    dateList: List[InlineKeyboardButton] = []
    buttons = []
    for dl in datesList:
        if len(dateList) == 2:  # 3 кнопки в ряд
            buttons.append(dateList)
            dateList = []

        button = InlineKeyboardButton(
            text=f'{dl[1]}',
            callback_data=f'cityData={dl[0]}|{dl[1]}'
        )
        dateList.append(button)

    buttons.append(dateList)
    # print(buttons)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def refreshButtons(number=1):
    keyboards = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Оновити',
                callback_data=f'update={number}'
            ),
            InlineKeyboardButton(
                text='З початку',
                callback_data='restart'
            )
        ]
    ])
    return keyboards
