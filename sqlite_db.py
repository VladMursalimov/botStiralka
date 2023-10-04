import sqlite3 as sq


async def db_connect():
    global db, cur

    db = sq.connect("base_users.db")
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS "
                "users(tg_id TEXT, tg_username TEXT, block TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS "
                "order_of_wash(tg_username TEXT, name TEXT, time TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS "
                "requests(tg_id TEXT, tg_username TEXT, name TEXT, lastname TEXT, block TEXT, time TEXT)")
    db.commit()


async def create_new_record(tg_username, user_name, user_end_time):
    global cur, db
    await db_connect()
    cur.execute("INSERT INTO order_of_wash VALUES (?, ?, ?)",
                (tg_username, user_name, user_end_time))
    db.commit()


async def register_new_user(tg_id, tg_username, user_block):
    global cur, db
    await db_connect()
    cur.execute("INSERT INTO users VALUES (?, ?, ?)",
                (tg_id, tg_username, user_block))
    db.commit()


async def check_user(user_id):
    global cur, db
    await db_connect()
    users_id = cur.execute("SELECT tg_id FROM users")
    for id in users_id:
        if str(id[0]) == str(user_id):
            return 1
    return 0


async def delete_from_order(tg_username):
    global cur, db
    await db_connect()
    cur.execute("DELETE FROM order_of_wash WHERE tg_username = ?",
                (tg_username,))
    db.commit()

async def get_user():
    global cur, db
    await db_connect()
    users = cur.execute("SELECT * FROM users")
    return users

async def get_order():
    global cur, db
    await db_connect()
    order = cur.execute("SELECT * FROM order_of_wash")
    return order

# admin
async def add_request(tg_id, tg_username, user_name, user_lastname, user_block, user_time):
    global cur, db
    await db_connect()
    cur.execute("INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?)",
                (tg_id, tg_username, user_name, user_lastname, user_block, user_time))
    db.commit()

async def check_user_request(user_id):
    global cur, db
    await db_connect()
    users_id = cur.execute("SELECT tg_id FROM requests")
    for id in users_id:
        if str(id[0]) == str(user_id):
            return 1
    return 0

async def get_requests():
    global cur, db
    await db_connect()
    requests = cur.execute("SELECT * FROM requests")
    return requests

async def delete_from_requests(tg_username):
    global cur, db
    await db_connect()
    cur.execute("DELETE FROM requests WHERE tg_username = ?",
                (tg_username,))
    db.commit()
# ------------------------


async def get_from_order(tg_username):
    global cur, db
    await db_connect()
    return cur.execute("SELECT tg_username FROM order_of_wash "
                       "WHERE tg_username = ?", (tg_username,))


async def is_in_order(tg_username):
    global cur, db
    await db_connect()
    users_un = cur.execute("SELECT tg_username "
                           "FROM order_of_wash")
    for un in users_un:
        if str(un[0]) == str(tg_username):
            return 1
    return 0
