from aiogram.fsm.context import FSMContext


async def getDataState(state: FSMContext):
    data = await state.get_data()
    dateNeed = data['date']
    timeNeed = data['time']
    serviceName = data['serviceName']
    servicePrice = data['servicePrice']
    textUser = f'Вибрана дата: <b>{dateNeed}</b>\r\nВибраний час: <b>{timeNeed}</b>\r\n' \
               f'Вибрана стрижка: <b>{serviceName} - {servicePrice}</b>\r\n'
    totalPrice = int(servicePrice)
    if 'addServe' in data:
        dictData = data['addServe']

        textUser += f'\r\nСупутні послуги:'

        for dd in dictData:
            for k, v in dd.items():
                textUser += f'\r\n<b>{k} {v}</b>'
                totalPrice += int(v)

        textUser += f'\r\n\r\nСума до оплати: <b>{totalPrice}</b>'
    return textUser


async def getDataForAdmin(state: FSMContext):
    data = await state.get_data()
    dateNeed = data['date']
    timeNeed = data['time']
    serviceName = data['serviceName']
    servicePrice = data['servicePrice']
    fullName = data['fullName']
    phone = data['phone']
    textUser = (f'<b>Потрібне підтвердження.</b>\r\n\r\n'
                f'Ім\'я: <b>{fullName}</b>\r\nТелефон: <b>{phone}</b>\r\n'
                f'Дата: <b>{dateNeed}</b>\r\nЧас: <b>{timeNeed}</b>\r\n'
                f'Стрижка: <b>{serviceName}</b>\r\nЦіна: <b>{servicePrice}</b>\r\n')
    totalPrice = int(servicePrice)
    if 'addServe' in data:
        dictData = data['addServe']

        textUser += f'\r\nСупутні послуги:'

        for dd in dictData:
            for k, v in dd.items():
                textUser += f'\r\n<b>{k} {v}</b>'
                totalPrice += int(v)

        textUser += f'\r\n\r\nСума до оплати: <b>{totalPrice}</b>'
    return textUser
