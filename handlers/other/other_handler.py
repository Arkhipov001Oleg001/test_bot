from aiogram import types, Dispatcher


# @dp.message_handler()
async def echo_bot(message: types.Message):
    await message.reply(message.text)


def register_handler_other(dp: Dispatcher):
    dp.register_message_handler(echo_bot)
