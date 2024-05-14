from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def getButtonFullName(name):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=name
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

