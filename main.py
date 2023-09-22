from aiogram import executor

import payment.pay
from settings.loader import dp
from handlers import *
from database import sqlite_db
from payment import *


async def on_startup(_):
    print('<<< БОТ ЗАПУЩЕН >>>')
    sqlite_db.sql_start()

default_command.register_handler_default(dp)
admin.register_handler_admin(dp)
payment.pay.register_pay(dp)
other.register_handler_other(dp)


# teach_pizza
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
