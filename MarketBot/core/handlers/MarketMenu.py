from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from MarketBot.core.Keyboards.MarketKeyboard import kbGetCategories, kbGetSubCategories, kbGetProducts, kbToCart, \
    kbGetOrder
from MarketBot.core.other.Request import Request


async def getHelp(message: Message, state: FSMContext, request: Request):
    await message.answer(
        'Привіт, звертайтесь по почті wild.savedo@gmail.com або @wytcorp',
        reply_markup=None)

async def getCategories(message: Message, request: Request):
    await message.answer(f'Привіт. Я помічник інтернет-магазину "Все і відразу!".'
                         f'Я допоможу тобі зробити покупку. Для початку давай ознайомлю тебе з каталогом!',
                         reply_markup=await kbGetCategories(request))


async def getSubCategories(call: CallbackQuery, bot: Bot, state: FSMContext, request: Request):
    if 'product' in call.data:
        # back=category|subcategory|product
        product = call.data.split('=')[1].split('|')
        category = call.message.reply_markup.inline_keyboard[-1][-1].callback_data.split('=')[1].split('|')[0]
        subcategory = call.message.reply_markup.inline_keyboard[-1][-1].callback_data.split('=')[1].split('|')[1]
        description, keyboard = await kbToCart(product, category, subcategory, request)
        return await call.message.edit_text(description, reply_markup=keyboard)
    elif 'back' in call.data:
        dataBack = call.data.split('=')[1]
        path = dataBack.split('|')
        if len(path) == 3:
            category = path[0]
            subcategory = path[1]
            return await call.message.edit_text(f'Подивимося, що я ще можу запропонувати',
                                                reply_markup=await kbGetProducts(category, subcategory, request))
        elif len(path) == 2:
            category = path[0]
            return await call.message.edit_text(f'Подивимося, що я ще можу запропонувати',
                                                reply_markup=await kbGetSubCategories(category, request))
        else:
            return await call.message.edit_text(f'Подивимося, що я ще можу запропонувати',
                                                reply_markup=await kbGetCategories(request))
    elif 'cart' in call.data:
        dataCart = call.data.split('=')[1]
        model = dataCart.split('|')[0]
        price = dataCart.split('|')[1]
        await call.answer(f'Чудово! Твій {model} за {price}$ додано до кошику!'
                          f'Щоб придбати товар, натисніть кнопку нижче.', show_alert=True)
        cartButton = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text='Кошик'
                    )
                ]
            ],
            resize_keyboard=True
        )

        await call.message.answer(f'Товар {model} за {price}$ додано до кошику', reply_markup=cartButton)
        await addToCart(state, model, price)

        return

    else:
        if await getBack(call.message.reply_markup.inline_keyboard):
            # back=category|subcategory
            # Отримуємо продукти, якщо є кнопка Назад back
            category = call.message.reply_markup.inline_keyboard[-1][-1].callback_data.split('=')[1].split('|')[0]
            categories = call.data
            keyboards = await kbGetProducts(category, categories, request)
        else:
            # back=category
            keyboards = await kbGetSubCategories(str(call.data), request)

        return await call.message.edit_reply_markup(reply_markup=keyboards)


async def getBack(keyboards: list[list]):
    for keyboard in keyboards:
        for element in keyboard:
            if 'back' in element.callback_data:
                return True

    return False


async def addToCart(state: FSMContext, model, price):
    data = await state.get_data()
    data[model] = price
    await state.set_data(data=data)


async def getCart(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data:
        await message.answer('Твій кошик порожній. Погортай каталог і вибери що-небудь.')
        return

    result = ''
    prices = 0
    for k, v in data.items():
        result += f'{k}    {v}\r\n'
        prices += int(v)

    text = f'Ок, ось твій кошик: \r\n\r\n {result}\r\n Загальна сума {prices}$'

    await message.answer(text, reply_markup=await kbGetOrder())
