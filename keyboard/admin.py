from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from configuration import config

from data.csdb import *


async def admin_menu():
	keyboard = InlineKeyboardMarkup(row_width = 2)
	gv_sub_btn = InlineKeyboardButton(text = "➡️ Выдать подписку", callback_data = "give_sub")
	tk_sub_btn = InlineKeyboardButton(text = "⬅️ Забрать подписку", callback_data = "take_sub")
	gv_adm_btn = InlineKeyboardButton(text = "🏅 Выдать админку", callback_data = "give_adm")
	tk_adm_btn = InlineKeyboardButton(text = "🕯 Забрать админку", callback_data = "take_adm")
	mass_send_btn = InlineKeyboardButton(text = "🪄 Рассылка", callback_data = "mass_send")
	stats_btn = InlineKeyboardButton(text = "📊 Статистика", callback_data = "stats")
	backup_btn = InlineKeyboardButton(text = "📑 Бэкап", callback_data = "get_bd")
	back_btn = InlineKeyboardButton(text = "⬅️ Обычное меню", callback_data = "back")

	keyboard.add(gv_sub_btn, tk_sub_btn, gv_adm_btn, tk_adm_btn, mass_send_btn, stats_btn, backup_btn, back_btn)

	return keyboard


async def return_menu():
	keyboard = InlineKeyboardMarkup()
	back_btn = InlineKeyboardButton(text = "⬅️ В главное меню", callback_data = "back_admin")

	keyboard.add(back_btn)

	return keyboard


