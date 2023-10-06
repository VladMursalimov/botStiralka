import asyncio
import datetime

import date_and_hours
import sqlite_db
import date_and_hours

async def main():
    print(await sqlite_db.get_orger_for_day(date_and_hours.get_current_day()))
    print(await sqlite_db.is_in_order("KevinBaconn", date_and_hours.get_current_day()))
    print(await sqlite_db.get_busy_times(date_and_hours.get_current_day()))
    print(date_and_hours.get_busy_times_by_hour(date_and_hours.get_current_hour()))
    print(date_and_hours.get_current_day())
    print(date_and_hours.get_current_day())
asyncio.run(main())
