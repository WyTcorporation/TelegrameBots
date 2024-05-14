from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def getButtons():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text='Охорона'
                ),
                KeyboardButton(
                    text='Комунальні послуги'
                )
            ],
            [
                KeyboardButton(
                    text='Нова + Укр пошта'
                ),
                KeyboardButton(
                    text='Амбулаторії'
                )
            ],
            [
                KeyboardButton(
                    text='Інтернет + Телебачення'
                ),
                KeyboardButton(
                    text='Маршрутки'
                ),
            ],
            [
                KeyboardButton(
                    text='Світло є?(в розробці)'
                ),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
