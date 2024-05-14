from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    stateFullName = State()
    stateNumber = State()
    stateIndication = State()
