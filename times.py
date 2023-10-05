import asyncio
import datetime

import sqlite_db
from main import get_current_day, get_current_month, get_current_hour, order_to_string
from sqlite_db import get_busy_times


async def main():
    await sqlite_db.create_new_record(tg_username="123",
                                      user_name="!@3",
                                      day=1,
                                      time_index=1,
                                      month=get_current_month())


asyncio.run(main())
