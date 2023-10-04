from aiogram.fsm.state import StatesGroup, State


class GettingRoomNumber(StatesGroup):
    getting_number = State()
