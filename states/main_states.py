from aiogram.dispatcher.filters.state import State, StatesGroup

class CardEnterRub(StatesGroup):
	card = State()

class CardEnterDollar(StatesGroup):
	card = State()

class CardEnterIvi(StatesGroup):
	card = State()

# ---- ADMIN STATES ---- #

class AdminGvSub(StatesGroup):
	user_data = State()

class AdminTkSub(StatesGroup):
	user_data = State()

class MakeAdmin(StatesGroup):
	user_data = State()

class KillAdmin(StatesGroup):
	user_data = State()

class SendText(StatesGroup):
	text = State()