import random
import datetime
import aiosqlite


path = "data/database_file/checkerBD.sqlite"

async def register_user(user_id, user_name, reg_date):
	async with aiosqlite.connect(path) as db:

		await db.execute("INSERT INTO users "
                         "(user_id, user_name, subscribe, until, reg_date, cooldown_check) "
                         "VALUES (?, ?, ?, ?, ?, ?)",
                         [user_id, user_name, "False", "Неактивна", reg_date, "Нет"])

		await db.commit()


async def buy_sub(user_id, period):
	async with aiosqlite.connect(path) as db:

		if user_id is str:
			user_id.replace("@", "")
			until = datetime.datetime.now() + datetime.timedelta(days=int(period))
			until = until.strftime("%d/%m/%Y %H:%M:%S")
			await db.execute(f"UPDATE users SET subscribe = 'Active' WHERE user_name = '{user_id}'")
			await db.execute(f"UPDATE users SET until = '{until}' WHERE user_name = '{user_id}'")
			await db.commit()
		else:
			until = datetime.datetime.now() + datetime.timedelta(days=int(period))
			until = until.strftime("%d/%m/%Y %H:%M:%S")
			await db.execute(f"UPDATE users SET subscribe = 'Active' WHERE user_id = {user_id}")
			await db.execute(f"UPDATE users SET until = '{until}' WHERE user_id = {user_id}")		
			await db.commit()

		return "Success"


async def del_sub(user_id):
	async with aiosqlite.connect(path) as db:

		if user_id is str:
			await db.execute(f"UPDATE users SET subscribe = 'Нет' WHERE user_name = {user_id}")
			await db.execute(f"UPDATE users SET until = 'Неактивна' WHERE user_name = {user_id}")
			await db.commit()
		else:
			await db.execute(f"UPDATE users SET subscribe = 'Нет' WHERE user_id = {user_id}")
			await db.execute(f"UPDATE users SET until = 'Неактивна' WHERE user_id = {user_id}")
			await db.commit()
		
		return "Success"


async def add_cooldown_check(user_id):
	async with aiosqlite.connect(path) as db:
		until = datetime.datetime.now() + datetime.timedelta(seconds=30)
		until = until.strftime("%d/%m/%Y %H:%M:%S")
		await db.execute(f"UPDATE users SET cooldown_check = '{until}' WHERE user_id = {user_id}")


async def get_user(user_id):
	async with aiosqlite.connect(path) as db:

		profile = await db.execute(f"SELECT * FROM users WHERE user_id = ?", (user_id,))

		return await profile.fetchone()


async def check_admin(user_id):
	async with aiosqlite.connect(path) as db:

		check = await db.execute(f"SELECT * FROM admins WHERE user_id = {user_id}")

		return await check.fetchone()


async def get_admins():
	async with aiosqlite.connect(path) as db:

		admins = await db.execute(f"SELECT * FROM admins")

		return await admins.fetchall()


async def add_admin(user_id):
	async with aiosqlite.connect(path) as db:
		await db.execute("INSERT INTO admins "
                         "(user_id) "
                         "VALUES (?)",
                         [user_id])

		await db.commit()


async def del_admin(user_id):
	async with aiosqlite.connect(path) as db:
		await db.execute(f"DELETE FROM admins WHERE user_id = {user_id}")
		await db.commit()


async def start_profit():
	async with aiosqlite.connect(path) as db:
		check = await db.execute("SELECT * FROM profit")
		if await check.fetchone() is None:
			money = 0
			await db.execute("INSERT INTO profit "
                	         "(money) "
                    	     "VALUES (?)",
                        	 [money])

			await db.commit()
			print("Inserted")
		else:
			print("check is not none")
			pass


async def update_profit(summa):
	async with aiosqlite.connect(path) as db:
		current = await db.execute("SELECT * FROM profit")
		current = await current.fetchone()
		await db.execute(f"UPDATE profit SET money = {current[0] + summa}")
		await db.commit()


async def select_profit():
	async with aiosqlite.connect(path) as db:
		profit = await db.execute("SELECT * FROM profit")
		return await profit.fetchone()


async def add_card(card, charge):
	async with aiosqlite.connect(path) as db:
		await db.execute("INSERT INTO cards "
                         "(card, charge) "
                         "VALUES (?, ?)",
                         [card, charge])

		await db.commit()


async def get_all_users():
	async with aiosqlite.connect(path) as db:
		users = await db.execute("SELECT * FROM users")
		return await users.fetchall()


async def get_count_cards():
	async with aiosqlite.connect(path) as db:
		cards = await db.execute("SELECT * FROM cards")
		return await cards.fetchall()


async def create_tables():
	async with aiosqlite.connect(path) as db:
		await db.execute("CREATE TABLE IF NOT EXISTS users("
						"user_id INTEGER, user_name TEXT, subscribe TEXT, "
						"until TEXT, reg_date TEXT, cooldown_check TEXT)")

		await db.execute("CREATE TABLE IF NOT EXISTS admins("
						"user_id INTEGER)")

		await db.execute("CREATE TABLE IF NOT EXISTS cards("
						"card TEXT, charge TEXT)")

		await db.execute("CREATE TABLE IF NOT EXISTS profit("
						"money INTEGER)")

		await db.commit()

