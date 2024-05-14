from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from LightOnOff.core.other import Request


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