from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from MarketBot.core.other.Request import Request


async def kbGetCategories(request: Request):
    buttons = []

    categories = await request.dbGetCategories()

    for cat in categories:
        button = InlineKeyboardButton(
            text=cat,
            callback_data=cat
        )
        buttons.append(button)

    keyboards = InlineKeyboardMarkup(inline_keyboard=[buttons])

    return keyboards


async def kbGetSubCategories(category, request: Request):
    buttons = []

    subcategories = await request.dbGetSubCategories(category)

    for subcat in subcategories:
        button = InlineKeyboardButton(
            text=subcat,
            callback_data=subcat
        )
        buttons.append(button)

    back = InlineKeyboardButton(
        text='Назад',
        callback_data=f'back={category}'
    )
    hallButtons = [buttons, [back]]

    return InlineKeyboardMarkup(inline_keyboard=hallButtons)


async def kbGetProducts(category, subcategory, request: Request):
    buttons = []

    products = await request.dbGetProducts(category, subcategory)

    for prod in products:
        button = InlineKeyboardButton(
            text=f'{prod[0]} ({prod[1]}$)',
            callback_data=f'product={prod[0]}|{prod[1]}'
        )
        buttons.append(button)

    back = InlineKeyboardButton(
        text='Назад',
        callback_data=f'back={category}|{subcategory}'
    )
    hallButtons = [buttons, [back]]

    return InlineKeyboardMarkup(inline_keyboard=hallButtons)


async def kbToCart(product, category, subcategory, request: Request):
    buttons = []

    product = await request.dbGetProductDescription(product, category, subcategory)
    model = product[0]
    price = product[1]
    description = product[2]
    button = InlineKeyboardButton(
        text=f'В кошику',
        callback_data=f'cart={model}|{price}'
    )
    buttons.append(button)

    button = InlineKeyboardButton(
        text=f'Назад',
        callback_data=f'back={category}|{subcategory}|{model}'
    )
    buttons.append(button)
    return description, InlineKeyboardMarkup(inline_keyboard=[buttons])


async def kbGetOrder():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Сплатити',
                    callback_data='getOrder'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Очистити корзину',
                    callback_data='clearCart'
                )
            ]
        ]
    )
