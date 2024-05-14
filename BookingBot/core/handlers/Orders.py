from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery

from BookingBot.core.Settings import settings
from BookingBot.core.other.GetDataText import dictLine
from BookingBot.core.other.Request import Request
from aiogram.enums import Currency

async def order(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    serviceName = data['serviceName']
    servicePrice = data['servicePrice']
    labeledPrice = [
        LabeledPrice(
            label=serviceName,
            amount=int(servicePrice) * 100
        )
    ]
    if 'addServe' in data:
        dd = data['addServe']

        for eld in dd:
            for k, v in eld.items():
                labeledPrice.append(
                    LabeledPrice(
                        label=k,
                        amount=int(v) * 100
                    )
                )

    title = f'Оплата послуг у салоні Мальвіна'
    desc = f'Тестова карта номер 1111 1111 1111 1026 12/22 CVC 000\r\n Після оплати з вами зв\'яжеться наш найшвидший менеджер протягом 5 хвилин'

    await bot.send_invoice(
        call.message.chat.id,
        title=title,
        description=desc,
        payload='telegram_order',
        provider_token=settings.bank.bankToken,
        currency=Currency.RUB,
        prices=labeledPrice,
        max_tip_amount=10000,
        suggested_tip_amounts=[1000, 2000, 3000, 4000],
        need_name=True,
        need_phone_number=True
    )


async def preCheckoutQuery(checkoutQuery: PreCheckoutQuery, bot: Bot, state: FSMContext):
    await bot.answer_pre_checkout_query(checkoutQuery.id, ok=True)
    line = dictLine(checkoutQuery.dict())
    result = f'<b>!!!ADMIN!!!</b>\r\n{dictLine(await state.get_data())}\r\n\r\n{line}'
    # await bot.send_message(settings.bots.adminId, text=result)
    await bot.send_message(checkoutQuery.from_user.id, text=result)


async def buyComplete(message: Message, state: FSMContext, request: Request):
    msg = f'Дякую за оплату {message.successful_payment.total_amount // 100}' \
          f' {message.successful_payment.currency}. \r\n' \
          f'Наш менеджер отримав заявку та вже набирає Ваш номер телефону'

    await message.answer(msg)

    data = await state.get_data()

    await request.dbChangeStatus('busy', data['date'], data['time'])
    await state.clear()
