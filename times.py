import asyncio

import data
import date_and_hours
import sqlite_db
import date_and_hours

async def main():
    print(await sqlite_db.get_busy_times(date_and_hours.get_current_datetime().day))
    print(date_and_hours.get_busy_times_after_hour(await sqlite_db.get_busy_times(date_and_hours.get_current_datetime().day)))
    print(date_and_hours.get_busy_times_by_hour(date_and_hours.get_current_hour()))
asyncio.run(main())
