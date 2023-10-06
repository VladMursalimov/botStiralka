import asyncio

import sqlite_db


async def main():
    await sqlite_db.add_column_tg_id_to_order_wash()


asyncio.run(main())
