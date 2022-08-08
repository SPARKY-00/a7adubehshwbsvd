from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from configuration import config

from data.csdb import *


async def main_menu(user_id):
	keyboard = InlineKeyboardMarkup(row_width = 2)
	start_btn = InlineKeyboardButton(text = "👁 Чекер", callback_data = "checker")
	profile_btn = InlineKeyboardButton(text = "🥷 Профиль", callback_data = "profile")
	subscribe_btn = InlineKeyboardButton(text = "💸 Купить подписку", callback_data = "subscribe")
	help_btn = InlineKeyboardButton(text = "❓ Инфо", callback_data = "help")
	chat_btn = InlineKeyboardButton(text = "💬 Чат", url = "https://t.me/joinchat/PxDHIZXfTfE4N2Yy")
	channel_btn = InlineKeyboardButton(text = "💎 Канал", url = "https://t.me/joinchat/NNkYreIb2LxlMGEy")

	keyboard.add(start_btn, profile_btn, subscribe_btn, help_btn, chat_btn, channel_btn)

	admins = await get_admins()

	if user_id in admins or user_id in config.admins:
		admin_btn = InlineKeyboardButton(text = "👑 Админ-панель", callback_data = "panel")
		keyboard.add(admin_btn)

	return keyboard


async def profile():
	keyboard = InlineKeyboardMarkup(row_width = 2)
	subscribe_btn = InlineKeyboardButton(text = "🔐 Подписаться", callback_data = "subscribe")
	back_btn = InlineKeyboardButton(text = "⬅️ Назад", callback_data = "back")

	keyboard.add(back_btn, subscribe_btn)

	return keyboard


async def subscribe():
	keyboard = InlineKeyboardMarkup(row_width = 1)
	subscribe_btn = InlineKeyboardButton(text = "🔐 Подписаться", callback_data = "subscribe")
	back_btn = InlineKeyboardButton(text = "⬅️ Назад", callback_data = "back")

	keyboard.add(subscribe_btn, back_btn)

	return keyboard


async def plan_menu():
	keyboard = InlineKeyboardMarkup(row_width = 3)
	one_day = InlineKeyboardButton(text = "💡 Один день", callback_data = "buy_sub one_day")
	three_days = InlineKeyboardButton(text = "🔮 Три дня", callback_data = "buy_sub three_days")
	seven_days = InlineKeyboardButton(text = "💎 Семь дней", callback_data = "buy_sub seven_days")
	back_btn = InlineKeyboardButton(text = "⬅️ Назад", callback_data = "back")

	keyboard.add(one_day, three_days, seven_days, back_btn)

	return keyboard


async def payment_methods(period):
	keyboard = InlineKeyboardMarkup(row_width = 2)
	qiwi_btn = InlineKeyboardButton(text = "🥝 Qiwi", callback_data = f"qiwi {period}")
	btc_btn = InlineKeyboardButton(text = "🧿 BTC Banker", callback_data = f"banker {period}")
	back_btn = InlineKeyboardButton(text = "⬅️ Назад", callback_data = "subscribe")

	keyboard.add(qiwi_btn, btc_btn, back_btn)

	return keyboard


async def payment_keyboard(send_requests, code, summa):
	keyboard = InlineKeyboardMarkup(row_width = 1)
	pay_btn = InlineKeyboardButton(text = "📄 Оплатить", url = send_requests)
	check_btn = InlineKeyboardButton(text = "🔁 Проверить оплату", callback_data = f"check_qiwi {code} {summa}")
	back_btn = InlineKeyboardButton(text = "⬅️ Назад", callback_data = "back")
    
	keyboard.add(pay_btn, check_btn, back_btn)
    
	return keyboard


async def check_menu():
	keyboard = InlineKeyboardMarkup(row_width = 1)
	auth_btn = InlineKeyboardButton(text = "[3DS] Авторизация", callback_data = "auth_check")
	charge_onerub_btn = InlineKeyboardButton(text = "[🇷🇺] Списание 1р", callback_data = "charge_one_rub")
	charge_fivedol_btn = InlineKeyboardButton(text = "[🌎] Списание 5$", callback_data = "charge_five_dol")
	faq_btn = InlineKeyboardButton(text = "❓ Описание режимов", callback_data = "check_faq")
	back_btn = InlineKeyboardButton(text = "⬅️ Назад", callback_data = "back")

	keyboard.add(auth_btn, charge_onerub_btn, charge_fivedol_btn, faq_btn, back_btn)

	return keyboard


async def return_all():
	keyboard = InlineKeyboardMarkup()
	back_btn = InlineKeyboardButton(text = "⬅️ Назад", callback_data = "back")

	keyboard.add(back_btn)

	return keyboard