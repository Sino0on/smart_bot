import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import requests
import json
import re



import request

url = "https://api.telegram.org/bot5346235377:AAGg1mWc4FPRxGn1GFcnOBcj75MMLlrAJlA/sendMessage"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.29.0",
    "Cookie": "csrftoken=XqYL4yFIf9Z7Ufe6nB6fg90TllF1OayZrJgebZFjjcdbY1q2rGVqiBIO7Ua82nD6",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}


class FSMAdmin(StatesGroup):
    username = State()
    password = State()
    password2 = State()
    age = State()
    email = State()
    tg = State()


class FSMNewsletters(StatesGroup):
    text = State()


a = {}
API_TOKEN = '5346235377:AAGg1mWc4FPRxGn1GFcnOBcj75MMLlrAJlA'

storage = MemoryStorage()
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


def postreg(asd):
    response = requests.post('http://127.0.0.1:8000/api/v1/register/', json=asd, headers=headers)
    print(response.ok)
    print(response.status_code)
    print(response.text)
    if str(response.ok) == 'False':
        return str(response.text)
    else:
        return 'OK'


@dp.message_handler(commands=['newsletter'], state=None)
async def cm_start(message: types.Message):
    rer = requests.get(' http://127.0.0.1:8000/api/v1/superaccountlist/').json()
    print(message.from_user.id)
    rdr = [i['tg'] for i in rer]
    print(rdr)
    if str(message.from_user.id) in rdr:
        await FSMNewsletters.text.set()
        await message.reply('Напишите текст который надо разослать')
    else:
        await message.reply('У вас недостаточно прав')


@dp.message_handler(state=FSMNewsletters.text)
async def load_username(message: types.Message, state: FSMContext):
    rer = requests.get(' http://127.0.0.1:8000/api/v1/accountlist/').json()
    rdr = [f"{i['tg']}" for i in rer]
    print(rdr)
    try:
        for i in rdr:
            response = requests.post(url, json={"text": message.text, "chat_id": i}, headers=headers)
    except:
        await message.reply('Что то пошло не так')
    await state.finish()
    await message.answer('Все ок')


@dp.message_handler(commands=['register'], state=None)
async def cm_start(message: types.Message):
    rer = requests.get(' http://127.0.0.1:8000/api/v1/accountlist/').json()
    rdr = [i['username_tg'] for i in rer]
    rdr2 = [i['tg'] for i in rer]
    if '@' + str(message.chat.username) in rdr or message.chat.id in rdr2:
        await message.reply('Ты уже зарегистрирован')
    elif len(str(message.chat.id)) <= 9:
        await FSMAdmin.username.set()
        await message.reply('Напиши свой username')
    else:
        await message.reply('Пожалуйста напишите мне в личку чтобы начать регистрцию')


@dp.message_handler(state=FSMAdmin.username)
async def load_username(message: types.Message, state: FSMContext):
    rer = requests.get(' http://127.0.0.1:8000/api/v1/accountlist/').json()
    rdr = [i['username'] for i in rer]
    print(rdr)
    if message.text not in rdr:
        async with state.proxy() as data:
            data['username'] = message.text
        await FSMAdmin.next()
        await message.reply('Придумай пароль')
    else:
        await message.reply('Такой никнейм уже есть, попробуй другой')


@dp.message_handler(state=FSMAdmin.password)
async def load_password(message : types.Message, state: FSMContext):
    if len(message.text) >= 6:
        async with state.proxy() as data:
            data['password'] = message.text
            if message.chat.username == '':
                data['username_tg'] = 'None'
            else:
                data['username_tg'] = '@' + str(message.chat.username)
        await FSMAdmin.next()
        await message.reply('Повтори пароль')
    else:
        await message.reply('Пожалуйста придумайте сложный пароль')


@dp.message_handler(state=FSMAdmin.password2)
async def load_password2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == data['password']:
            data['password2'] = message.text
            data['tg'] = str(message.chat.id)
            data['last_name'] = str(message.chat.last_name)
            data['first_name'] = str(message.chat.first_name)
            await message.reply('Сколько вам лет?')
            await FSMAdmin.next()
        else:
            await message.reply('Пароли не схожи, Повторите попытку')


@dp.message_handler(state=FSMAdmin.age)
async def load_password2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await message.reply('Введи свою почту')
    await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.email)
async def load_email(message: types.Message, state: FSMContext):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(regex, message.text):
        async with state.proxy() as data:
            data['email'] = message.text
            asd = dict(data)
            print(asd)
        await state.finish()
        await message.reply('Ожидайте')
        await message.reply(str(postreg(asd)))
    else:
        await message.reply('Некорректный email')


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


# @dp.message_handler()
# async def echo(message: types.Message):
#
#     await message.answer(message.chat.id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
