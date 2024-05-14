from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def adminButton(date, time, userId):
    keyboards = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Підтвердити',
                callback_data=f'adminConfirm={date}|{time}|{userId}'
            ),
            InlineKeyboardButton(
                text='Відхилити',
                callback_data=f'adminCancel={date}|{time}|{userId}'
            )
        ]
    ])
    return keyboards
