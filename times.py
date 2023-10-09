import asyncio
import datetime

import date_and_hours
import sqlite_db
import date_and_hours
import strings


async def main():
    print(strings.get_users_to_string(await sqlite_db.get_users(), 1))


asyncio.run(main())
