import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import requests
import json

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
    email = State()
    first_name = State()
    last_name = State()
    tg = State()

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
    print(response.text)

@dp.message_handler(commands=['register'], state=None)
async def cm_start(message : types.Message):
    await FSMAdmin.username.set()
    await message.reply('Напиши свой username')


@dp.message_handler(state=FSMAdmin.username)
async def load_username(message: types.Message, state: FSMContext):
    rer = requests.post('http://127.0.0.1:8000/api/v1/accountlist/')
    if message.text not in [rer]:
        async with state.proxy() as data:
            data['username'] = message.text
        await FSMAdmin.next()
        await message.reply('Придумай пароль')
    else:
        await message.reply('Повторите')

@dp.message_handler(state=FSMAdmin.password)
async def load_password(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    await FSMAdmin.next()
    await message.reply('Повтори пароль')


@dp.message_handler(state=FSMAdmin.password2)
async def load_password2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password2'] = message.text
    await FSMAdmin.next()
    await message.reply('Введи свою почту')


@dp.message_handler(state=FSMAdmin.email)
async def load_email(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    await FSMAdmin.next()
    await message.reply('Введи свое имя')


@dp.message_handler(state=FSMAdmin.first_name)
async def load_first_name(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text
    await FSMAdmin.next()
    await message.reply('Введи свою фамилию')


@dp.message_handler(state=FSMAdmin.last_name)
async def load_last_name(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text
        data['tg'] = str(message.chat.id)
        global a
        asd = dict(data)
    print(asd)
    await state.finish()
    await message.reply('Ожидайте')
    postreg(asd)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
