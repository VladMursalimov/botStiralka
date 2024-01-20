import asyncio

import sqlite_db
import date_and_hours


async def main():
    await sqlite_db.delete_banned_user(5555)
    await sqlite_db.add_banned_user(5555, date_and_hours.plus_day_to_current_time(7 * 3))
    print(await sqlite_db.get_banned_users(5555))


asyncio.run(main())
