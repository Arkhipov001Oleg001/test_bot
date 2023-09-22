import sqlite3 as sq
from aiogram.types import InputMediaPhoto
from settings.loader import bot


def sql_start():
    global base, cur
    base = sq.connect('clothes')
    cur = base.cursor()
    if base:
        print('Успешное подключение к БД')
    base.execute('CREATE TABLE IF NOT EXISTS menu('
                 'name TEXT,'
                 ' description TEXT,'
                 ' size TEXT,'
                 ' price TEXT,'
                 ' img TEXT,'
                 ' color TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO  menu VALUES (?,?,?,?,?,?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu ').fetchall():
        media_list = []
        for i in ret[-2].split('*')[:-1]:
            new_media = InputMediaPhoto(type='photo', media=i)
            media_list.append(new_media)
        photo_last = InputMediaPhoto(type='photo', media=ret[-2].split('*')[-1], caption=f'{ret[0]}\n'
                                                                                         f'Описание: {ret[1]}\n'
                                                                                         f'Размеры: {ret[2]}\n'
                                                                                         f'Цена: {ret[3]}\n'
                                                                                         f'Цвет: {ret[-1]}\n')
        media_list.append(photo_last)
        await bot.send_media_group(message.from_user.id, media=media_list)


async def sql_read_2():
    return cur.execute('SELECT * FROM menu ').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()
