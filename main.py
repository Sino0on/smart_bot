import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import requests
import json
import re

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

import request

markup = InlineKeyboardMarkup()

url = "https://api.telegram.org/bot5346235377:AAGg1mWc4FPRxGn1GFcnOBcj75MMLlrAJlA/sendMessage"

host_url = 'http://127.0.0.1:8000/'

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


def authuser(tgid):
    rer = requests.get(f'{host_url}api/v1/accountlist/').json()
    rdr = [f"{i['tg']}" for i in rer]
    if str(tgid) in rdr:
        return True
    else:
        return False


def authadmin(tgid):
    rer = requests.get(f'{host_url}api/v1/superaccountlist/').json()
    rdr = [f"{i['tg']}" for i in rer]
    if str(tgid) in rdr:
        return True
    else:
        return False


def postreg(asd):
    response = requests.post(f'{host_url}api/v1/register/', json=asd, headers=headers)
    if str(response.ok) == 'False':
        return str(response.text)
    else:
        return 'OK'


@dp.message_handler(commands=['newsletter'], state=None)
async def cm_start(message: types.Message):
    rer = requests.get(f'{host_url}/api/v1/superaccountlist/').json()
    print(message.from_user.id)
    rdr = [i['tg'] for i in rer]
    print(rdr)
    if str(message.from_user.id) in rdr:
        await FSMNewsletters.text.set()
        await message.reply('Напишите текст который надо разослать всем')
    else:
        await message.reply('У вас недостаточно прав')


@dp.message_handler(state=FSMNewsletters.text)
async def load_username(message: types.Message, state: FSMContext):
    rer = requests.get(f'{host_url}api/v1/accountlist/').json()
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
async def register(message: types.Message):
    rer = requests.get(f'{host_url}api/v1/accountlist/').json()
    rdr = [i['username_tg'] for i in rer]
    rdr2 = [i['tg'] for i in rer]
    print(rer)
    if str(message.from_user.id) in rdr2:
        await message.reply('Ты уже зарегистрирован')
    elif len(str(message.chat.id)) <= 11:
        await FSMAdmin.username.set()
        await message.reply('Началась регистрация, пожалуйста напиши свой username')
    else:
        await message.reply('Пожалуйста напишите мне в личку чтобы начать регистрцию')


@dp.message_handler(state=FSMAdmin.username)
async def load_username(message: types.Message, state: FSMContext):
    rer = requests.get(f'{host_url}api/v1/accountlist/').json()
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
async def load_password(message: types.Message, state: FSMContext):
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
            await message.reply('Сколько тебе лет? 💫')
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


@dp.message_handler(commands=['application'])
async def course_detail(message: types.Message, id):
    print(True)
    markup = InlineKeyboardMarkup(row_width=2)
    courses = requests.get(f'{host_url}api/v1/courselist/').json()
    for i in courses:
        if i['id'] == id:
            print('DAstan')
            course = i
            break
        else:
            course = 'no'

    inline_btn_1 = InlineKeyboardButton('Записаться 📩', callback_data=f'create-{id}')
    markup.add(inline_btn_1)
    inline_btn_1 = InlineKeyboardButton('Назад 🚫', callback_data=f'courses')
    markup.add(inline_btn_1)
    print(message)
    if authadmin(message.chat.id):
        inline_btn_1 = InlineKeyboardButton('Группы', callback_data=f'groups-{id}')
        markup.add(inline_btn_1)
    try:
        await message.answer_photo(photo=f'{course["image"]}', caption=f'{course["title"]}\n{course["description"]}\nКурс длиться {course["duration"]}\nКаждое занятие по {course["hour"]} часа\nКаждый месяц по {course["price"]}', reply_markup=markup)
    except:
        await message.answer(f'{course["title"]}\n{course["description"]}\nКурс длиться {course["duration"]}\nКаждое занятие по {course["hour"]} часа\nКаждый месяц по {course["price"]}', reply_markup=markup)


@dp.message_handler(commands=['meeting'])
async def meet_detail(message: types.Message, id):
    markup = InlineKeyboardMarkup(row_width=2)
    meeting = requests.get(f'{host_url}api/v1/meetslist/').json()
    print(meeting)
    for i in meeting:
        if i['id'] == id:
            meeting_detail = i
            break
        else:
            meet_detail = 'no'
    print(id)
    print(message)
    if authadmin(message['chat']['id']):
        inline_btn_1 = InlineKeyboardButton('Просмотреть заявки', callback_data=f'applicationmet-{id}')
        markup.add(inline_btn_1)
    inline_btn_1 = InlineKeyboardButton('Записаться 📩', callback_data=f'createmet{id}')
    markup.add(inline_btn_1)
    inline_btn_1 = InlineKeyboardButton('Назад 🚫', callback_data=f'meeting')
    markup.add(inline_btn_1)
    try:
        await message.answer_photo(photo=f'{meeting_detail["image"]}', caption=f'{meeting_detail["title"]}\n{meeting_detail["description"]}\n', reply_markup=markup)
    except:
        await message.answer(f'{meeting_detail["title"]}\n{meeting_detail["description"]}\n', reply_markup=markup)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2)
    if authuser(message.from_user.id):
        inline_btn_1 = InlineKeyboardButton('Курсы 💻', callback_data='courses')
        inline_btn_2 = InlineKeyboardButton('🎊 Мероприятия 🎊', callback_data='meeting')
        markup.add(inline_btn_1)

        markup.add(inline_btn_2)
        await message.answer(
            '''Привет👋, Я Зи 
Aссистент компании Zetroom💡
Я помогу как тут все устроено
Если ты хочешь оставить заявку на курсы то нажми \n"Курсы 💻"
А если ты хочешь посмотреть наши мероприятия то нажми \n"🎊 Мероприятия 🎊"''', reply_markup=markup)
    else:
        inline_btn_1 = InlineKeyboardButton('Зарегистрироваться 📲', callback_data='register')
        markup.add(inline_btn_1)
        await message.answer('Привет, меня зовут Зи, я представляю компанию ZetRoom💡\nДля того чтобы просмотреть продолжить нужно для начало зарегистрироваться\nДля этого нажмите "Зарегистрироваться 📲"', reply_markup=markup)


@dp.message_handler(commands=['admin'])
async def admin_welcome(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2)
    if authadmin(message.from_user.id):
        print(message)
        inline_btn_1 = InlineKeyboardButton('Курсы', callback_data='courses')
        markup.add(inline_btn_1)
        inline_btn_1 = InlineKeyboardButton('Заявки', callback_data='applicationlist')
        markup.add(inline_btn_1)
        await message.answer("Приветсвую Админ", reply_markup=markup)
    else:
        await message.answer('Вы не админ')


@dp.message_handler(commands=['dastan'])
async def accept(message: types.Message, data):
    await message.delete()
    markup = InlineKeyboardMarkup(row_width=2)
    print(data)
    markup.add(InlineKeyboardButton('Принять ✅', callback_data=f'acceptapplication-{data["id"]}'))
    markup.add(InlineKeyboardButton('Отказ 🚫', callback_data=f'Ignore-{data["id"]}'))
    await message.answer(f'{data["account"]["username"]}, {data["account"]["username_tg"]}\n{data["course"]["title"]}',
                         reply_markup=markup)


@dp.message_handler()
async def accept(message: types.Message):
    print(message.text)
    if message.text == 'ZetRoom':
        await bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAEFUjFi1-ZJ87hEAozUIuD8HnKkuFnfswACY2kAAuCjggfNiOgW_zbDYikE')
        await message.reply(text='Вы разблокировали пасхалку🥳🥳')


@dp.callback_query_handler()
async def process_callback(call: types.CallbackQuery):
    print(call.data)
    courses = requests.get(f'{host_url}api/v1/courselist/').json()
    meetings = requests.get(f'{host_url}api/v1/meetslist/').json()
    if call.data == 'register':
        await register(message=call.message)
    if call.data == 'courses':
        print(call.message)
        markup = InlineKeyboardMarkup(row_width=2)

        markup.clean()
        for i in courses:
            inline_btn_1 = InlineKeyboardButton(i['title'], callback_data=i['id'])
            markup.add(inline_btn_1)
        await bot.send_message(chat_id=call.from_user.id, text='Все наши курсы', reply_markup=markup)
    if 'groups' in call.data:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        rer = requests.get(f'{host_url}api/v1/grouplistbot').json()
        print(call.data)
        markup = InlineKeyboardMarkup()
        markup.clean()
        group = {}
        for i in rer:
            if str(i['id']) == call.data.split('-')[-1]:
                inline_btn_1 = InlineKeyboardButton(i['title'], callback_data=f'groupdetail-{i["id"]}')
                markup.add(inline_btn_1)
        await bot.send_message(chat_id=call.from_user.id, text='Группы', reply_markup=markup)
    if 'groupdetail' in call.data:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        rer = requests.get(f'{host_url}api/v1/grouplist').json()
        markup = InlineKeyboardMarkup(row_width=2)
        for i in rer:
            if call.data.split('-')[-1] == str(i['id']):
                group = i
                break
        for i in group['students']:
            inline_btn_1 = InlineKeyboardButton(i['username'], callback_data=f'student-{i["id"]}')
            markup.add(inline_btn_1)
        await bot.send_message(chat_id=call.from_user.id, text='Студенты', reply_markup=markup)
    if 'applicationmet' in call.data:
        # await bot.delete_message(call.from_user.id, call.message.message_id)
        markup = InlineKeyboardMarkup(row_width=2)
        rer = requests.get(f'{host_url}api/v1/meetapplication?meeting={call.data.split("-")[-1]}').json()
        print(rer)
        for i in rer:
            rar = requests.get(f'{host_url}api/v1/accountlist?id={i["account"]}').json()
            print(rar[0]['username'])
            print(i["account"])
            inline_btn_1 = InlineKeyboardButton(rar[0]['username'], callback_data=f'student-{i["account"]}')
            markup.add(inline_btn_1)
        await bot.send_message(chat_id=call.from_user.id, text='Все заявки на курсы', reply_markup=markup)
    if call.data == 'meeting':

        markup = InlineKeyboardMarkup(row_width=2)

        markup.clean()
        for i in meetings:
            inline_btn_1 = InlineKeyboardButton(i['title'], callback_data=f"meetdetail-{i['id']}")
            markup.add(inline_btn_1)
        await bot.send_message(chat_id=call.from_user.id, text='Мероприятия', reply_markup=markup)
    if 'meetdetail' in str(call.data):
        for i in meetings:
            if str(call.data).split('-')[-1] == str(i['id']):
                await bot.delete_message(call.from_user.id, call.message.message_id)
                await meet_detail(message=call.message, id=i['id'])
    if str(call.data).isdigit():
        for i in courses:
            if str(call.data) == str(i['id']):
                await bot.delete_message(call.from_user.id, call.message.message_id)
                await course_detail(message=call.message, id=i['id'])
    if 'createmet' in str(call.data):
        for i in meetings:
            if str(call.data) == f'createmet{i["id"]}':
                markup = InlineKeyboardMarkup(row_width=2)
                account = call.from_user.id
                payload = {
                    "account": int(account),
                    "meeting": i['id'],
                }
                print(payload)
                response = requests.post(f'{host_url}api/v1/applicationmeetcreate/', json=payload)
                print(response.ok)
                if response.ok == True:
                    await bot.delete_message(call.from_user.id, call.message.message_id)
                    # inline_btn_1 = InlineKeyboardButton('Домой', callback_data='home')
                    # inline_btn_2 = InlineKeyboardButton('Курсы', callback_data='courses')
                    # markup.add(inline_btn_1, inline_btn_2)
                    await bot.answer_callback_query(callback_query_id=call.id,
                                                    text=f'Вы оставили заявку на мероприятие {i["title"]}',
                                                    show_alert=True)
                    # await bot.send_message(text=f'Вы оставили заявку на {i["title"]}', chat_id=call.from_user.id, reply_markup=markup)

                else:
                    await bot.delete_message(call.from_user.id, call.message.message_id)
                    # inline_btn_1 = InlineKeyboardButton('Домой', callback_data='home')
                    # inline_btn_2 = InlineKeyboardButton('Курсы', callback_data='courses')
                    # markup.add(inline_btn_1, inline_btn_2)
                    await bot.answer_callback_query(callback_query_id=call.id,
                                                    text='Ошибка, походу вы уже отправляли заявку, либо тут моя ошибка',
                                                    show_alert=True)
                    # await bot.send_message(text='Ошибка, походу вы уже отправляли заявку, либо тут моя ошибка', chat_id=call.from_user.id)
    elif 'create' in str(call.data):
        for i in courses:
            print(call.data)
            if str(call.data) == f'create-{i["id"]}':
                markup = InlineKeyboardMarkup(row_width=2)
                print('da')
                print(type(call.from_user.id))
                rer = requests.get(f'{host_url}api/v1/accountlist/').json()
                account = call.from_user.id
                print(rer)
                # for j in rer:
                #     if j['tg'] == call.from_user.id:
                #         account = j['id']

                print(int(account))
                payload = {
                    "account": int(account),
                    "course": i['id'],
                }
                print(payload)
                response = requests.post(f'{host_url}api/v1/applicationcreate/', json=payload)
                print(response.ok)
                if response.ok == True:
                    await bot.delete_message(call.from_user.id, call.message.message_id)
                    # inline_btn_1 = InlineKeyboardButton('Домой', callback_data='home')
                    # inline_btn_2 = InlineKeyboardButton('Курсы', callback_data='courses')
                    # markup.add(inline_btn_1, inline_btn_2)
                    await bot.answer_callback_query(callback_query_id=call.id,
                                                    text=f'Вы оставили заявку на {i["title"]}', show_alert=True)
                    # await bot.send_message(text=f'Вы оставили заявку на {i["title"]}', chat_id=call.from_user.id, reply_markup=markup)

                else:
                    await bot.delete_message(call.from_user.id, call.message.message_id)
                    # inline_btn_1 = InlineKeyboardButton('Домой', callback_data='home')
                    # inline_btn_2 = InlineKeyboardButton('Курсы', callback_data='courses')
                    # markup.add(inline_btn_1, inline_btn_2)
                    await bot.answer_callback_query(callback_query_id=call.id,
                                                    text='Ошибка, походу вы уже отправляли заявку, либо тут моя ошибка',
                                                    show_alert=True)
                    # await bot.send_message(text='Ошибка, походу вы уже отправляли заявку, либо тут моя ошибка', chat_id=call.from_user.id)

    if str(call.data) == 'applicationlist':
        await call.message.delete()
        markup = InlineKeyboardMarkup(row_width=1)
        rer = requests.get(f'{host_url}api/v1/applicationlist/').json()
        for i in rer:
            inline_btn_1 = InlineKeyboardButton(f'{i["account"]["username"]} {i["course"]["title"]}',
                                                callback_data=f"applicationfor-{i['id']}")
            markup.add(inline_btn_1)
        await bot.send_message(text='Заявки', chat_id=call.from_user.id, reply_markup=markup)
    if call.data == 'home':
        await call.message.delete()
        await send_welcome(message=call.message)
    if 'student' in call.data:
        rer = requests.get(f'{host_url}api/v1/accountlist/?id={call.data.split("-")[-1]}').json()
        if str(rer) != '[]':
            await bot.send_message(chat_id=call.from_user.id, text=rer)
    if 'applicationfor' in call.data:
        rer = requests.get(f'{host_url}api/v1/applicationlist/').json()
        for i in rer:
            if str(i['id']) == str(call.data).split('-')[-1]:
                await accept(message=call.message, data=i)
    if 'acceptapplication' in call.data:
        rer = requests.get(f'{host_url}api/v1/grouplist/').json()
        rar = requests.get(f'{host_url}api/v1/applicationlist/').json()
        for i in rar:
            if str(i["id"]) == call.data.split('-')[-1]:
                print('dasd')
                course = i['course']['id']
                break
        markup = InlineKeyboardMarkup(row_width=2)
        await call.message.delete()
        print(rer)
        print(course)
        for i in rer:
            if course == i['course']:
                print('dastan')
                btn = InlineKeyboardButton(text=f'{i["title"]}',
                                           callback_data=f'addcoursegroup-{i["id"]}-{call.data.split("-")[-1]}')
                markup.add(btn)
        btn = InlineKeyboardButton(text=f'Создать новую группу', callback_data=f'addnewcoursegroup')
        markup.add(btn)
        await bot.send_message(text='В какую группу желаете добавить?', chat_id=call.from_user.id, reply_markup=markup)
    if 'addnewcoursegroup' == call.data:
        await bot.send_message(text='Извините но эта функция на разработке', chat_id=call.from_user.id)
    if 'addcoursegroup' in call.data:
        rar = requests.get(f'{host_url}api/v1/applicationlist/').json()
        for i in rar:
            if str(i["id"]) == call.data.split('-')[-1]:
                application = i
                break
        rer = requests.get(f'{host_url}api/v1/grouplistbot').json()
        print(call.data)
        for i in rer:
            if str(i['id']) == call.data.split('-')[-2]:
                group = i
        await bot.delete_message(call.from_user.id, call.message.message_id)
        print(application)
        if application['account']['id'] not in group['students']:
            group['students'].append(application['account']['id'])
            print(group)
            response = requests.request(method='PUT',
                                        url=f"{host_url}api/v1/groupupdate/{str(call.data.split('-')[-2])}", json=group)
            print(response.text)
            deler = requests.delete(f"{host_url}api/v1/applicationdelete/{application['id']}").json()
            print(deler)
            await bot.send_message(chat_id=application['account']['tg'], text=f'Вас добавили в группу {group["title"]}\nОжидайте дальнейщих указаний 🥳')
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text='Студент успешно добавлен🥳',
                                            show_alert=True)
        deler = requests.delete(f"{host_url}api/v1/applicationdelete/{application['id']}")
        print(deler)
        await bot.answer_callback_query(callback_query_id=call.id,
                                        text='Студент уже в группе 😓',
                                        show_alert=True)
        if 'Ignore' in call.data:
            rar = requests.get(f'{host_url}api/v1/applicationlist/').json()
            for i in rar:
                if i["id"] == call.data.split('-')[-1]:
                    application = i
            print(application)
            deler = requests.delete(f"{host_url}api/v1/applicationdelete/{application['id']}")
            print(deler)


# @dp.message_handler()
# async def echo(message: types.Message):
#
#     await message.answer(message.chat.id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
