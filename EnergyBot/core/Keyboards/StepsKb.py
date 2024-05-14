from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from typing import List
from EnergyBot.core.other.Request import Request


async def kbGetStart():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text='Інформація'
                ),
                KeyboardButton(
                    text='Перевірити показники'
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

async def contractButtons():
    keyboards = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Загальна інформація',
                callback_data='allInfo'
            )
        ],
        [
            InlineKeyboardButton(
                text='Додати показники',
                callback_data='adding'
            ),
            InlineKeyboardButton(
                text='Скинути налаштування',
                callback_data='clearing'
            )
        ]
    ])
    return keyboards

async def clearingButtons():
    keyboards = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Так',
                callback_data='clearingTrue'
            ),
            InlineKeyboardButton(
                text='Ні',
                callback_data='clearingFalse'
            )
        ]
    ])
    return keyboards

async def infoButtons():
    keyboards = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Послуги та тарифи',
                callback_data='tariff'
            )
        ],
        [
            InlineKeyboardButton(
                text='Планові і аварійні відключення',
                callback_data='emergencyShutdowns'
            )
        ],
        [

            InlineKeyboardButton(
                text='Відсутня електроенергія?',
                callback_data='noElectricity'
            )
        ],
        [

            InlineKeyboardButton(
                text='Контактний номер для комунікації Вашого району',
                callback_data='communication'
            )
        ],
        [

            InlineKeyboardButton(
                text='Загальні контакти',
                callback_data='contacts'
            )
        ]
    ])
    return keyboards

async def tariffButtons():
    keyboards = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Тарифи',
                callback_data='tariffs'
            )
        ],
        [
            InlineKeyboardButton(
                text='Послуги з підключення/відключення',
                callback_data='tariffOnOff'
            )
        ],
        [
            InlineKeyboardButton(
                text='Послуги з технічної перевірки',
                callback_data='tariffTech'
            )
        ],
        [

            InlineKeyboardButton(
                text='Послуги параметризації лічильників',
                callback_data='tariffCounters'
            )
        ],
        [

            InlineKeyboardButton(
                text='Інші послуги',
                url='https://www.dtek-kem.com.ua/ua/services-tariffs'
            ),
            InlineKeyboardButton(
                text='Назад',
                callback_data='back'
            )
        ]
    ])
    return keyboards


