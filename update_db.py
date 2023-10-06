import asyncio

import sqlite_db


async def main():
    # await sqlite_db.add_column_tg_id_to_order_wash()
    # await sqlite_db.delete_ilnaz()
    await sqlite_db.update_db_id()


asyncio.run(main())
