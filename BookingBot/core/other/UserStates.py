from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    stateFullName = State()
    stateDate = State()
    stateTime = State()
    stateService = State()
    stateAddService = State()
    stateGetPhone = State()
