from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    name_st = State()
    number_st = State()

class ChangeAdminInfo(StatesGroup):
    get_channel_id = State()
    get_channel_url = State()
    mailing = State()
    utm = State()
    change_message = State()
    bonus_amount = State()
    bonus_info = State()
