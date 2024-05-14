from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def deleteButton(keyboard: InlineKeyboardMarkup, elDel):
    newKeyboard = []
    for keys in keyboard.inline_keyboard:
        timeKey = []

        for key in keys:
            if elDel not in key.callback_data:
                if 'Дякую не потрібно' in key.text:
                    key.text = 'Мабуть, вистачить'
                timeKey.append(key)

        newKeyboard.append(timeKey)

    keyboards = InlineKeyboardMarkup(inline_keyboard=newKeyboard)

    if len(keyboards.inline_keyboard[0]) >= 1:
        return keyboards
    else:
        return await buyButton()


async def buyButton():
    keyboards = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Оформити замовлення',
                callback_data='application'
            ),
            InlineKeyboardButton(
                text='Перейти до оплати',
                callback_data='order'
            )
        ],
        [
            InlineKeyboardButton(
                text='Очистити корзину',
                callback_data='clearCart'
            )
        ]
    ])
    return keyboards
