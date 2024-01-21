import datetime
import sqlite3 as sq

from strings import order_to_string


async def db_connect():
    global db, cur
    # path = "/home/kevin12312312/mysite/"
    path = ""
    db = sq.connect(path + "new.db")
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users(tg_id int, tg_username TEXT, block TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS order_of_wash"
                "(tg_username TEXT, name TEXT, time_index int, day int, tg_id int)")
    cur.execute("CREATE TABLE IF NOT EXISTS washed_users"
                "(id INTEGER PRIMARY KEY AUTOINCREMENT, tg_username TEXT, name TEXT, time_index int, day int, tg_id int)")
    cur.execute("CREATE TABLE IF NOT EXISTS banned_users"
                "(tg_id int, day int)")

    db.commit()


async def delete_user(tg_id):
    global cur, db
    await db_connect()
    cur.execute("DELETE FROM users WHERE tg_id = ?", (tg_id,))
    db.commit()


async def get_name_and_block_by_id(tg_id):
    global cur, db
    await db_connect()
    res = cur.execute("SELECT block FROM users WHERE tg_id = ?", (tg_id,)).fetchall()
    if res: return res[-1][0]
    return ""


async def delete_banned_user(tg_id: int):
    global cur, db
    await db_connect()
    cur.execute("DELETE FROM banned_users WHERE tg_id = ?", (tg_id,))
    db.commit()


async def get_banned_users(tg_id: int):
    global cur, db
    await db_connect()
    users_id = cur.execute("SELECT * FROM banned_users WHERE tg_id = ?", (tg_id,)).fetchall()
    return users_id


async def add_banned_user(tg_id: int, end_ban_time: int):
    global cur, db
    await db_connect()
    cur.execute("INSERT INTO banned_users VALUES (?, ?)", (tg_id, end_ban_time))
    db.commit()


async def add_column_tg_id_to_order_wash():
    global cur, db
    await db_connect()
    cur.execute("ALTER TABLE order_of_wash ADD COLUMN tg_id")
    db.commit()


async def create_new_record(tg_username, user_name, time_index, day=0, tg_id=0):
    global cur, db
    await db_connect()
    cur.execute("INSERT INTO order_of_wash VALUES (?, ?, ?, ?, ?)", (tg_username, user_name, time_index, day, tg_id))
    cur.execute("INSERT INTO washed_users (tg_username, name, time_index, day, tg_id) VALUES (?, ?, ?, ?, ?)",
                (tg_username, user_name, time_index, day, tg_id))
    db.commit()


async def register_new_user(tg_id, tg_username, user_block):
    global cur, db
    await db_connect()
    cur.execute("INSERT INTO users VALUES (?, ?, ?)", (tg_id, tg_username, user_block))
    db.commit()


async def check_user(user_id):
    global cur, db
    await db_connect()
    users_id = cur.execute("SELECT tg_id FROM users")
    for id in users_id:
        if str(id[0]) == str(user_id):
            return 1
    else:
        return 0


async def delete_from_order(tg_id):
    global cur, db
    await db_connect()
    cur.execute("DELETE FROM order_of_wash WHERE tg_id = ?", (tg_id,))
    cur.execute(f"delete from washed_users WHERE tg_id = {tg_id} AND id = ( select max(id) from washed_users )")
    db.commit()


async def get_order():
    global cur, db
    await db_connect()
    order = cur.execute("SELECT * FROM order_of_wash ORDER BY time_index + day + month")
    return order


async def get_orger_for_day(day):
    global cur, db
    await db_connect()
    print(datetime.datetime.fromtimestamp(day))
    order = cur.execute(f"SELECT * FROM order_of_wash WHERE day = {day} ORDER BY time_index")
    return order.fetchall()


async def get_from_order(tg_id):
    global cur, db
    await db_connect()
    return cur.execute("SELECT tg_username FROM order_of_wash WHERE tg_id = ?", (tg_id,))


async def get_users():
    global cur, db
    await db_connect()
    return cur.execute("SELECT * FROM users").fetchall()


async def get_user_room(tg_id):
    global cur, db
    await db_connect()
    return cur.execute("SELECT block FROM users WHRER tg_id = ", (tg_id,)).fetchone()


# async def delete_ilnaz():
#     global cur, db
#     await db_connect()
#     cur.execute("DELETE FROM order_of_wash WHERE name = ?", ("Ильназ",))
#     db.commit()

async def is_in_order(tg_id, day):
    global cur, db
    await db_connect()
    users_un = cur.execute(f"SELECT tg_id FROM order_of_wash WHERE day >= {day}")
    for un in users_un:
        if str(un[0]) == str(tg_id):
            return 1
    else:
        return 0


async def get_busy_times(day: int):
    global cur, db
    await db_connect()
    busy_times = list(map(lambda x: x[0], cur.execute(
        f"SELECT time_index FROM order_of_wash WHERE day = {day}").fetchall()))
    return set(busy_times)


# async def clean_time():
#     global cur, db
#     await db_connect()
#     print("!23")
#     records = cur.execute(
#         f"SELECT * FROM order_of_wash").fetchall()
#     print(order_to_string(records, ""))
#     for row in records:
#         tg_username, tg_name, time_index, day, tg_id = row
#
#         new_day = datetime.datetime.fromtimestamp(day)
#         print(new_day, tg_username, time_index)
#         new_day = new_day.replace(hour=0)
#         print(int(new_day.timestamp()))
#         cur.execute(f'UPDATE order_of_wash SET day = {int(new_day.timestamp())} WHERE tg_username = "{tg_username}"')
#     db.commit()


async def is_limited(tg_id, day):
    global cur, db
    await db_connect()
    cur.execute(f"SELECT COUNT(tg_id) as count FROM washed_users WHERE day >= {day - 86400 * 30} AND tg_id = {tg_id}")
    n = cur.fetchone()[0]
    if n > 6:
        return 1
    else:
        return 0


async def update_db_id():
    global cur, db
    await db_connect()
    records = cur.execute(f"SELECT tg_id, tg_username FROM users").fetchall()
    for record in records:
        cur.execute(f'UPDATE order_of_wash SET tg_id = {record[0]} WHERE tg_username = "{record[1]}"')
    db.commit()
