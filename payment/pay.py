import os
from dotenv import load_dotenv, find_dotenv
from settings.loader import bot, dp
from aiogram import types, Dispatcher


if not find_dotenv():
    exit('Переменные окружения для ОПЛАТЫ не загружены т.к. отсутствует файл .env')
else:
    load_dotenv()


# @dp.message_handler(commands=['pay'])
async def payment(message: types.Message):
    print(os.getenv('PAYMENT_TOKEN'))
    await bot.send_invoice(chat_id=message.chat.id,
                           title='Покупка курса',
                           description='Описание',
                           provider_token=os.getenv('PAYMENT_TOKEN'),
                           currency='rub',
                           prices=[types.LabeledPrice('УРА', 100 * 100)],
                           start_parameter='test_bot',
                           payload='buy_stake_package')


async def pre_check(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


async def good_payment(message: types.Message):
    await bot.send_message(message.from_user.id, f'Платёж успешно выполнен: {message.successful_payment.order_info}')


def register_pay(dp: Dispatcher):
    dp.register_message_handler(payment, commands=['pay'])
    dp.register_pre_checkout_query_handler(pre_check, lambda query: True)
    dp.register_message_handler(good_payment, content_types=types.ContentType.SUCCESSFUL_PAYMENT)
