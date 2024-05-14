from aiogram.types import CallbackQuery
from aiogram import Bot
from BookingBot.core.other.Request import Request


async def answerReserve(call: CallbackQuery, request: Request, bot: Bot):
    # adminConfirm={date}|{time}|{userId}
    # adminCancel={date}|{time}|{userId}
    typeAnswer = call.data.split('=')[0]
    data = call.data.split('=')[1].split('|')
    date = data[0]
    time = data[1]
    userId = data[2]

    text = call.message.text.replace('Потребує підтвердження.', '')

    if 'adminConfirm' == typeAnswer:
        await request.dbChangeStatus('busy', date, time)
        msgUser = f'ВАШЕ ЗАМОВЛЕННЯ ПІДТВЕРДЖЕНО\r\n\r\n{text}'
        msgAdmin = f'!!!ADMIN!!! ЗАМОВЛЕННЯ ПІДТВЕРДЖЕНО\r\n\r\n{text}'
    else:
        msgUser = f'ВАШЕ ЗАМОВЛЕННЯ ВІДМОВЛЕНО\r\n\r\n{text}'
        msgAdmin = f'!!!ADMIN!!! ЗАМОВЛЕННЯ ВІДМОВЛЕНО\r\n\r\n{text}'

    await call.message.edit_text(msgAdmin, reply_markup=None)
    await bot.send_message(userId, msgUser)
