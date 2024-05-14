from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    stateFullName = State()
    stateArea = State()
    stateCityText = State()
    stateCity = State()
    stateStreet = State()
    stateStatus = State()
