import re

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from BookingBot.core.Keyboards.AdminButtons import adminButton
from BookingBot.core.Keyboards.EditButtons import deleteButton, buyButton
from BookingBot.core.Keyboards.serviceButtons import kbGetService, kbGetAddService
from BookingBot.core.Keyboards.TextButtons import getButtonFullName
from BookingBot.core.Keyboards.UserButtons import kbGetDate, kbGetTime
from BookingBot.core.other.Request import Request
from BookingBot.core.other.UserStates import UserStates
from BookingBot.core.other.DataForUser import getDataState, getDataForAdmin
from BookingBot.core.Settings import settings


async def getHelp(message: Message, state: FSMContext, request: Request):
    await message.answer(
        'Привіт, звертайтесь по почті wild.savedo@gmail.com або @wytcorp',
        reply_markup=None)
    await request.addUser(message.from_user.id,
                            message.from_user.first_name,
                            message.from_user.last_name,
                            message.from_user.last_name,
                            message.from_user.username)

async def getName(message: Message, state: FSMContext, request: Request):
    await message.answer('Привіт, Я помічник салону краси Мальвіна. Як я можу до Вас звертатися?',
                         reply_markup=await getButtonFullName(message.from_user.full_name))
    await state.set_state(UserStates.stateFullName)
    # print(json.dumps(message.dict(), default=str))
    await request.addUser(message.from_user.id,
                          message.from_user.first_name,
                          message.from_user.last_name,
                          message.from_user.last_name,
                          message.from_user.username)


async def getDate(message: Message, state: FSMContext, request: Request):
    await message.answer(f'Приємно познайомитися {message.text}, виберіть час', reply_markup=await kbGetDate(request))
    await state.update_data(fullName=message.text)
    await state.set_state(UserStates.stateDate)
    # print(await state.get_data())


async def getTime(call: CallbackQuery, state: FSMContext, request: Request):
    dateNeed = call.data.split('=')[1]
    await call.message.edit_text(f'Вибрана дата: <b>{dateNeed}</b>\r\nТепер виберіть час:',
                                 reply_markup=await kbGetTime(request, dateNeed))
    await state.update_data(date=dateNeed)
    await state.set_state(UserStates.stateTime)


async def getService(call: CallbackQuery, state: FSMContext, request: Request):
    data = await state.get_data()
    dateNeed = data['date']
    timeNeed = call.data.split('=')[1]
    await state.update_data(time=timeNeed)
    await state.set_state(UserStates.stateService)
    await call.message.edit_text(f'Вибрана дата: <b>{dateNeed}</b>\r\nВибраний час: <b>{timeNeed}</b>\r\n'
                                 f'Тепер оберіть стрижку:',
                                 reply_markup=await kbGetService())
    await request.dbChangeStatus('process', dateNeed, timeNeed)


async def getAddService(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    dateNeed = data['date']
    timeNeed = data['time']
    serviceNeed = call.data.split('=')[1].split('|')
    serviceName = serviceNeed[0]
    servicePrice = serviceNeed[1]
    await state.update_data(serviceName=serviceName, servicePrice=servicePrice)
    await state.set_state(UserStates.stateAddService)
    await call.message.edit_text(f'Вибрана дата: <b>{dateNeed}</b>\r\nВибраний час: <b>{timeNeed}</b>\r\n'
                                 f'Вибрана стрижка: <b>{serviceName} - {servicePrice}</b>\r\n'
                                 f'Пропонуємо Вам також супутні послуги:',
                                 reply_markup=await kbGetAddService())


async def handleAddService(call: CallbackQuery, state: FSMContext):
    add = []

    data = await state.get_data()

    if 'addServe' in data:
        add = data['addServe']

    serviceNeed = call.data.split('=')[1].split('|')
    serviceName = serviceNeed[0]
    servicePrice = serviceNeed[1]
    add.append({serviceName: servicePrice})
    await state.update_data(addServe=add)
    keyboard = await deleteButton(call.message.reply_markup, call.data)
    await call.message.edit_text(await getDataState(state), reply_markup=keyboard)


async def application(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f'Дякуємо за замовлення, залиште свій номер телефону.')
    await state.set_state(UserStates.stateGetPhone)


async def checkPhone(message: Message, state: FSMContext, bot: Bot):
    # result = re.match(r'((\+38)?\(?\d{3}\)?[\s\.-]?(\d{7}|\d{3}[\s\.-]\d{2}[\s\.-]\d{2}|\d{3}-\d{4}))',
    result = re.match(r'^\+?3?8?(0\d{9})$',
                      message.text)
    if not result:
        return await message.answer(f'Це не схоже на номер телефону, спробуйте ще раз.')

    await state.update_data(phone=message.text)

    await message.answer(f'Дякую за ваше замовлення. Ваші дані передані менеджеру, Очікуйте на дзвінок.')
    data = await state.get_data()
    dateNeed = data['date']
    timeNeed = data['time']

    await bot.send_message(chat_id=settings.bots.adminId, text=await getDataForAdmin(state),
                           reply_markup=await adminButton(dateNeed, timeNeed, message.from_user.id))
    await state.clear()


async def addServiceChancel(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(await getDataState(state), reply_markup=await buyButton())


async def clearCart(call: CallbackQuery, state: FSMContext, request: Request):
    data = await state.get_data()
    dateNeed = data['date']
    timeNeed = data['time']
    await request.dbChangeStatus('free', dateNeed, timeNeed)
    await state.clear()
    await call.message.edit_text(f'Кошик очищений. Щоб почати заново напишіть /start', reply_markup=None)

