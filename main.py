import asyncio
import logging
import sqlite3
import random
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from magic_filter import F
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import Text
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from key import *
from dp_qwest import COUNT

CONT = COUNT + 1
TOKEN = "6196860612:AAEkhfus9mLqL_j2Ome-tepgK1jGXAUgOLY"

router = Router()

list_user = {}
last_list_user = {}

con_2 = sqlite3.connect("users.db")
cursor_2 = con_2.cursor()

con_1 = sqlite3.connect("qwest.db")
cursor_1 = con_1.cursor()



@router.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_1,
        resize_keyboard=True,
    )
    await message.answer("Сыграем?", reply_markup=keyboard)



#@router.message(Command("restart"))
#async def cmd_start(message: types.Message):
#    await message.reply("Прогресс обнулён!", reply_markup=types.ReplyKeyboardRemove())
#
#    id_user = int(message.from_user.id)
#
#    cursor_2.execute('SELECT id FROM users WHERE id = (?)', [id_user])
#    if cursor_2.fetchone() != None:
#        count_true_user = cursor_2.fetchall()[3]
#        cursor_1.execute()
#        cursor_2.execute('DELETE FROM users WHERE id = (?)', [id_user])
#        con_2.commit()
#
#
#    keyboard = types.ReplyKeyboardMarkup(
#        keyboard=kb_1,
#        resize_keyboard=True,
#    )
#    await message.answer("Сыграем?", reply_markup=keyboard)
#

@router.message(Text("Пройти квест!"))
async def reg_user(message: types.Message):
    '''
    регистрация игрока в базе + стартовый набор задач, если ещё не играл
    '''
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
    id_user = int(message.from_user.id)
    cursor_2.execute('SELECT id FROM users WHERE id = (?)', [id_user])
    if cursor_2.fetchone() == None:
        """
        определение списка задач
        """
        count_qwest = list(range(1, CONT))
        list_qwest = str(count_qwest).replace(',', '')[1:-1]
        data = [id_user, list_qwest, 0]
        """
        регистрация пользователя в базе
        """
        cursor_2.execute("INSERT INTO users (id, num, true) VALUES (?,?,?)", data)
        con_2.commit()

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_2,
        resize_keyboard=True,
    )
    await message.answer("Поехали?", reply_markup=keyboard)


@router.message(Text("Получить вопрос!"))
async def choice_qwest(message: types.Message):
    await message.reply("Вот тебе один факт", reply_markup=types.ReplyKeyboardRemove())
    id_user = message.from_user.id
    if id_user not in list_user:

        cursor_2.execute('SELECT * FROM users WHERE id = (?)', [id_user])
        try:
            num_qwest = int(random.choice(cursor_2.fetchone()[2].split()))
        except:
            await message.answer("Поздравляю, ты прошел квест до конца!")
            foto = 'data/finish.jpg'
            qwest_image = FSInputFile(foto)
            await message.answer_photo(
                qwest_image,
                caption=""
            )

            cursor_2.execute('SELECT * FROM users WHERE id = (?)', [id_user])
            count_true = cursor_2.fetchone()[3]
            procent = int((count_true / COUNT) * 100)
            await message.answer("Поздравляю, ты прошел квест до конца!\n"
                                 f"Правильных ответов {procent}%")

            return

        cursor_1.execute('SELECT * FROM qwest WHERE № = (?)', [num_qwest])
        data_qwest = cursor_1.fetchone()
        image_qwest = data_qwest[1]
        image_answer = data_qwest[2]
        image_info = data_qwest[3]
        qwest_ans = data_qwest[4]
        data = {'num_qwest': num_qwest,
                'image_qwest': image_qwest,
                'image_answer': image_answer,
                'image_info': image_info,
                'qwest_ans': qwest_ans
                }
        list_user[id_user] = data
        """
        удаляем текущую задачу из списка задач игрока
        """
        cursor_2.execute('SELECT * FROM users WHERE id = (?)', [id_user])
        a = cursor_2.fetchone()[2].replace(str(num_qwest), '')
        cursor_2.execute('UPDATE users SET num = (?) WHERE id = (?)', [a, id_user])
        con_2.commit()
        cursor_2.execute('SELECT * FROM users WHERE id = (?)', [id_user])

    else:
        image_qwest = list_user[id_user]['image_qwest']
    qwest_image = FSInputFile('data/image/' + image_qwest)
    await message.answer_photo(
        qwest_image,
        caption=""
    )
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_3,
        resize_keyboard=True,
    )
    await message.answer("Что скажешь?", reply_markup=keyboard)


@router.message(Text("Правда"))
async def true_ans(message: types.Message):
    global con_1, con_2, cursor_1, cursor_2
    await message.reply("Ответ принят!", reply_markup=types.ReplyKeyboardRemove())

    id_user = message.from_user.id
    image_qwest = list_user[id_user]['image_answer']
    qwest_image = FSInputFile('data/image/' + image_qwest)
    await message.answer_photo(
        qwest_image,
        caption=""
    )
    if list_user[id_user]['qwest_ans'] == 'True':
        num_qwest = list_user[id_user]['num_qwest']
        cursor_1.execute('UPDATE qwest SET true = true + 1 WHERE № = (?)', [num_qwest])
        con_1.commit()
        cursor_1.execute('SELECT * FROM qwest WHERE № = (?)', [num_qwest])
        count_true = cursor_1.fetchone()[5]
        cursor_2.execute("SELECT * FROM users")
        count_user = len(cursor_2.fetchall())
        cursor_2.execute('UPDATE users SET true = true + 1 WHERE id = (?)', [id_user])
        con_2.commit()
        await message.reply("Поздравляю, ты ответил верно!\n"
                            f"С вопросом справились{int((count_true / count_user) * 100)}% пользователей")
    else:
        num_qwest = list_user[id_user]['num_qwest']
        cursor_1.execute('UPDATE qwest SET false = false + 1 WHERE № = (?)', [num_qwest])
        con_1.commit()
        cursor_1.execute('SELECT * FROM qwest WHERE № = (?)', [num_qwest])
        count_true = cursor_1.fetchone()[5]
        cursor_2.execute("SELECT * FROM users")
        count_user = len(cursor_2.fetchall())
        await message.reply("К сожалению ответ неверный!\n"
                            f"С вопросом справились {int((count_true / count_user) * 100)}% пользователей")
    last_list_user[id_user] = list_user[id_user]

    del list_user[id_user]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_4,
        resize_keyboard=True,
    )
    await message.answer("Что дальше?", reply_markup=keyboard)


@router.message(Text("Ложь"))
async def fals_ans(message: types.Message):
    global con_1, con_2, cursor_1, cursor_2
    await message.reply("Ответ принят!", reply_markup=types.ReplyKeyboardRemove())

    id_user = message.from_user.id
    image_qwest = list_user[id_user]['image_answer']
    qwest_image = FSInputFile('data/image/' + image_qwest)
    await message.answer_photo(
        qwest_image,
        caption=""
    )
    if list_user[id_user]['qwest_ans'] == 'False':
        num_qwest = list_user[id_user]['num_qwest']
        cursor_1.execute('UPDATE qwest SET true = true + 1 WHERE № = (?)', [num_qwest])
        con_1.commit()

        cursor_1.execute('SELECT * FROM qwest WHERE № = (?)', [num_qwest])
        count_true = cursor_1.fetchone()[5]
        cursor_2.execute("SELECT * FROM users")
        count_user = len(cursor_2.fetchall())
        cursor_2.execute('UPDATE users SET true = true + 1 WHERE id = (?)', [id_user])
        con_2.commit()
        await message.reply("Поздравляю, ты ответил верно!\n"
                            f"С вопросом справились{int((count_true / count_user) * 100)}% пользователей")
    else:
        num_qwest = list_user[id_user]['num_qwest']
        cursor_1.execute('UPDATE qwest SET false = false + 1 WHERE № = (?)', [num_qwest])
        con_1.commit()
        cursor_1.execute('SELECT * FROM qwest WHERE № = (?)', [num_qwest])
        count_true = cursor_1.fetchone()[5]
        cursor_2.execute("SELECT * FROM users")
        count_user = len(cursor_2.fetchall())
        await message.reply("К сожалению ответ неверный!\n"
                            f"С вопросом справились {int((count_true / count_user) * 100)}% пользователей")
    last_list_user[id_user] = list_user[id_user]
    del list_user[id_user]


    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_4,
        resize_keyboard=True,
    )
    await message.answer("Что дальше?", reply_markup=keyboard)


@router.message(Text("Узнать подробности!"))
async def true_ans(message: types.Message):
    await message.reply("Надеюсь эта информация тебе пригодиться!", reply_markup=types.ReplyKeyboardRemove())
    id_user = message.from_user.id
    image_info = last_list_user[id_user]['image_info']
    qwest_image = FSInputFile('data/image/' + image_info)
    await message.answer_photo(
        qwest_image,
        caption=""
    )
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_2,
        resize_keyboard=True,
    )
    await message.answer("Играем дальше?", reply_markup=keyboard)


async def main():
    global dp
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    bot = Bot(TOKEN, parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
