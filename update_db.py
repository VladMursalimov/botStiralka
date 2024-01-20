import asyncio

import date_and_hours
import sqlite_db


async def main():
    print(date_and_hours.plus_day_to_current_time(-3))
    # await sqlite_db.delete_ilnaz()


asyncio.run(main())
