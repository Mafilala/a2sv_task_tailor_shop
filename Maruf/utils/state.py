from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    name = State()
    phone_number = State()
    type_ = State()
    waist = State()
    hip = State()
    length = State()
    chest_width = State()
    body_length = State()
    sleeve_length = State()
    price = State()
    due_date = State()