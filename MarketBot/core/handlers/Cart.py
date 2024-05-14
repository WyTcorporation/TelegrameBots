from aiogram import Bot
from aiogram.enums import Currency
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, LabeledPrice, PreCheckoutQuery

from MarketBot.core.Settings import settings
from MarketBot.core.other.Request import Request


async def clearCart(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await call.message.answer(f'{call.message.chat.first_name}, твій кошик порожній.')
    await bot.answer_callback_query(call.id)


async def sendInvoice(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    price = []

    for k, v in data.items():
        price.append(
            LabeledPrice(
                label=k,
                amount=int(v) * 100
            )
        )

    title = f'Покупка в магазині "Все й одразу"'
    desc = f'Тестова карта номер 1111 1111 1111 1026 12/22 CVC 000\r\n Після оплати менеджер зв\'яжеться з Вами'

    await bot.send_invoice(
        call.message.chat.id,
        title=title,
        description=desc,
        payload='telegram_order',
        provider_token=settings.bank.bankToken,
        currency=Currency.RUB,
        prices=price,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        is_flexible=True
    )


async def preCheckoutQuery(pcq: PreCheckoutQuery, bot: Bot, state: FSMContext):
    await bot.answer_pre_checkout_query(pcq.id, ok=True)
    result = dictLine(pcq.dict())
    line = dictLine(await state.get_data()) + f'\r\n\r\n{result}'
    await bot.send_message(settings.bots.adminId, line)


async def buyComplete(message: Message, bot: Bot):
    msg = (
        f'Дякую про оплату {message.successful_payment.total_amount // 100} {message.successful_payment.currency}, \r\n'
        f'Наш менеджер отримав Вашу заявку і вже набирає Ваш номер телефону')
    await message.answer(msg)


def dictLine(dicts):
    result = []

    def listDict(d):
        for k, v in d.items():
            if isinstance(v, dict):
                listDict(v)
            else:
                result.append(f'{k.capitalize()}: {v}')

    listDict(dicts)
    return ';\r\n'.join(result)
