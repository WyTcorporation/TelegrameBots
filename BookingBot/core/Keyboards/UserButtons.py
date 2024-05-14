from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from BookingBot.core.other.Request import Request


async def kbGetDate(request: Request):
    datesList = await request.dbGetDate()
    dateList: List[InlineKeyboardButton] = []
    buttons = []
    for dl in datesList:
        if len(dateList) == 3:  # 3 кнопки в ряд
            buttons.append(dateList)
            dateList = []

        button = InlineKeyboardButton(
            text=dl,
            callback_data=f'reserveDate={dl}'
        )
        dateList.append(button)

    buttons.append(dateList)
    # print(buttons)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def kbGetTime(request: Request, dateNeeded):
    timesList = await request.dbGetTime(dateNeeded)
    timeList: List[InlineKeyboardButton] = []
    buttons = []
    for tl in timesList:
        if len(timeList) == 3:  # 3 кнопки в ряд
            buttons.append(timeList)
            timeList = []

        button = InlineKeyboardButton(
            text=tl,
            callback_data=f'reserveTime={tl}'
        )
        timeList.append(button)

    buttons.append(timeList)
    # print(buttons)
    return InlineKeyboardMarkup(inline_keyboard=buttons)
