import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import requests
import json
import re

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, InputFile

import request

ras = ''

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
    first_name = State()
    last_name = State()
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


def rassylka(text, group=None, student=None, course=None, groupmet=None, all=False):
    if group:
        for i in group[0]["students"]:
            json = {"text": text, "chat_id": i["tg"]}
            rer = requests.post(url=url, json=json)
            print(rer)
    elif student:
        json = {"text": text, "chat_id": student["tg"]}
        rer = requests.post(url=url, json=json)
    elif course:
        for i in course:
            json = {"text": text, "chat_id": i["tg"]}
            rer = requests.post(url=url, json=json)
    elif groupmet:
        for i in groupmet:
            print(i)
            student = requests.get(f'{host_url}api/v1/accountlist/?id={i["account"]}').json()
            print(student)
            json = {"text": text, "chat_id": student[0]["tg"]}
            rer = requests.post(url=url, json=json)
    elif all:
        rer = requests.get(f'{host_url}api/v1/accountlist').json()
        for i in rer:
            json = {"text": text, "chat_id": i["tg"]}
            rer = requests.post(url=url, json=json)


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
        return '🎊Вы успешно прошли регистрацию🎉'


@dp.message_handler(commands=['newsletter'], state=None)
async def rassylka_start(message: types.Message):
    rer = requests.get(f'{host_url}api/v1/superaccountlist?json').json()
    print(message)
    # print(message.reply_markup.inline_keyboard[-1][0])
    print(message.reply_markup.inline_keyboard[-1][0]["callback_data"])

    print(message.reply_markup.inline_keyboard)
    for i in message.reply_markup.inline_keyboard:
        print(i)
        if 'send_letter' in i[0]["callback_data"]:
            global ras
            ras = i[0]["callback_data"]
            break
    print(ras)
    # print(type(message.reply_markup.inline_keyboard[1][0]))
    rdr = [i['tg'] for i in rer]
    # print(rdr)
    if str(message.chat.id) in rdr:
        await FSMNewsletters.text.set()
        await message.reply('Напишите текст который надо разослать')
    else:
        await message.reply('У вас недостаточно прав')


@dp.message_handler(state=FSMNewsletters.text)
async def load_username(message: types.Message, state: FSMContext):
    print(ras+" send")
    if ras == 'send_letter_all':
        try:
            rassylka(message.text, all=True)
            print('Yes')
            await message.answer('Сообщение отправлено😜')
        except:
            await message.reply('Что то пошло не так')
    elif 'send_letter_student' in ras:
        try:
            student = requests.get(f'{host_url}api/v1/accountlist/?id={ras.split("-")[-1]}').json()
            print(student)
            rassylka(message.text, student=student[0])
            print('Yes')
            await message.answer('Сообщение отправлено😜')
        except:
            await message.reply('Что то пошло не так')
    elif 'send_letter_group' in ras:
        rer = requests.get(f'{host_url}api/v1/grouplist/?course={ras.split("-")[-1]}').json()
        try:
            print(rer)
            rassylka(message.text, group=rer)
            print('Yes')
            await message.answer('Сообщение отправлено😜')
        except:
            await message.reply('Что то пошло не так')
    elif 'send_letter_meet' in ras:
        rer = requests.get(f'{host_url}api/v1/meetapplication/?meeting={ras.split("-")[-1]}').json()
        try:
            print(rer)
            rassylka(message.text, groupmet=rer)
            print('Yes')
            await message.answer('Сообщение отправлено😜')
        except:
            await message.reply('Что то пошло не так')
    # elif ''
    await state.finish()



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
        regex = "^[A-Za-z][A-Za-z0-9_]{3,29}$"
        if re.search(regex, message.text):
            async with state.proxy() as data:
                data['username'] = message.text
            await FSMAdmin.next()
            await message.reply('Придумай пароль от 8 букв и цифр')
        else:
            await message.answer('Пропиши правильный username от 3 символов, без пробела и без эмодзи ❌')
    else:
        await message.reply('Такой никнейм уже есть, попробуй другой ❌')


@dp.message_handler(state=FSMAdmin.password)
async def load_password(message: types.Message, state: FSMContext):
    regex = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
    if re.fullmatch(regex, message.text):
        await message.delete()
        async with state.proxy() as data:
            data['password'] = message.text
            if message.chat.username == '':
                data['username_tg'] = 'None'
            else:
                data['username_tg'] = '@' + str(message.chat.username)
        await FSMAdmin.next()
        await message.answer('Повтори пароль')
    else:
        await message.reply('Пожалуйста придумай сложный пароль от 8 букв и цифр 😭')


@dp.message_handler(state=FSMAdmin.password2)
async def load_password2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == data['password']:
            await message.delete()
            data['password2'] = message.text
            data['tg'] = str(message.chat.id)
            data['last_name'] = str(message.chat.last_name)
            data['first_name'] = str(message.chat.first_name)
            await message.answer('Сколько тебе лет? 💫')
            await FSMAdmin.next()
        else:
            await message.reply('Пароли не схожи, Повторите попытку ❌')


@dp.message_handler(state=FSMAdmin.age)
async def load_password2(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 3 < int(message.text) < 80:
        async with state.proxy() as data:
            data['age'] = message.text
        await message.reply('Введи свою почту📩')
        await FSMAdmin.next()
    elif not message.text.isdigit():
        await message.reply('Пропиши только цифры ❌')
    elif int(message.text) > 80:
        await message.reply('Ты живой? Повтори еще раз ❌')


@dp.message_handler(state=FSMAdmin.email)
async def load_email(message: types.Message, state: FSMContext):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(regex, message.text):

        async with state.proxy() as data:
            data['email'] = message.text
            asd = dict(data)
            print(asd)
        await FSMAdmin.next()
        await message.answer('Введи свое имя')
    else:
        await message.reply('Некорректный email ❌')

    @dp.message_handler(state=FSMAdmin.first_name)
    async def load_first_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['first_name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи свою фамилию')

    @dp.message_handler(state=FSMAdmin.last_name)
    async def load_last_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['last_name'] = message.text
            data['tg'] = str(message.chat.id)
            global a
            asd = dict(data)
        print(asd)
        await state.finish()
        await message.reply('Ожидайте')
        await message.reply(str(postreg(asd)))
        await send_welcome(message=message)
        postreg(asd)


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
        inline_btn_1 = InlineKeyboardButton('Группы 🔑', callback_data=f'groups-{id}')
        markup.add(inline_btn_1)
        inline_btn_1 = InlineKeyboardButton('Разослать всем сообщение 🔑', callback_data=f'send_letter_course-{id}')
        markup.add(inline_btn_1)
    inline_btn_1 = InlineKeyboardButton('Домой', callback_data=f'home')
    markup.add(inline_btn_1)
    print(course['image'])
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
        inline_btn_1 = InlineKeyboardButton('Просмотреть заявки 🔑', callback_data=f'applicationmet-{id}')
        markup.add(inline_btn_1)
        inline_btn_1 = InlineKeyboardButton('Разослать всем сообщение 🔑', callback_data=f'send_letter_meet-{id}')
        markup.add(inline_btn_1)
    inline_btn_1 = InlineKeyboardButton('Записаться 📩', callback_data=f'createmet{id}')
    markup.add(inline_btn_1)
    inline_btn_1 = InlineKeyboardButton('Назад 🚫', callback_data=f'meeting')
    markup.add(inline_btn_1)
    inline_btn_1 = InlineKeyboardButton('Домой', callback_data=f'home')
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
        inline_btn_2 = InlineKeyboardButton('📅 Мероприятия 🎊', callback_data='meeting')
        markup.add(inline_btn_1)
        markup.add(inline_btn_2)
        markup.add(
            InlineKeyboardButton('Наш сайт 🌐', url='https://surik00.gitbooks.io/aiogram-lessons/content/'),
            InlineKeyboardButton('Наш инстаграмм 🌐', url='https://surik00.gitbooks.io/aiogram-lessons/content/'))
        markup.add(InlineKeyboardButton('Наш менеджер', url='t.me//Sino0on'))

        await message.answer_photo(
            photo='https://sun9-west.userapi.com/sun9-3/s/v1/ig2/keq9VmIk4Xa8sYN_SBimS6R-prRhnh2IFmK3gIXUG91A4_MbMlYPTvilDOQyXpHpILL9GhqGIufoeJm5SgkA-P_7.jpg?size=2160x2160&quality=96&type=album',
            caption='''Привет👋, Я Зи 
Aссистент компании Zetroom💡
Я помогу тебе разобраться как тут все устроено
Если ты хочешь оставить заявку на курсы то нажми \n"Курсы 💻"
А если ты хочешь посмотреть наши мероприятия то нажми \n"📅 Мероприятия 🎊"''', reply_markup=markup)
    else:
        inline_btn_1 = InlineKeyboardButton('Зарегистрироваться 📲', callback_data='register')
        markup.add(inline_btn_1)
        await message.answer_photo(photo='https://sun9-west.userapi.com/sun9-3/s/v1/ig2/keq9VmIk4Xa8sYN_SBimS6R-prRhnh2IFmK3gIXUG91A4_MbMlYPTvilDOQyXpHpILL9GhqGIufoeJm5SgkA-P_7.jpg?size=2160x2160&quality=96&type=album', caption='Привет, меня зовут Зи, я представляю компанию ZetRoom💡\nДля того, чтобы продолжить просмотр, необходимо предварительно зарегистрироваться 📲"', reply_markup=markup)


@dp.message_handler(commands=['admin'])
async def admin_welcome(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2)
    if authadmin(message.from_user.id):
        print(message)
        inline_btn_1 = InlineKeyboardButton('Курсы 🔑', callback_data='courses')
        markup.add(inline_btn_1)
        inline_btn_1 = InlineKeyboardButton('Заявки 🔑', callback_data='applicationlist')
        markup.add(inline_btn_1)
        inline_btn_1 = InlineKeyboardButton('Разослать всем сообщение 🔑', callback_data=f'send_letter_all')
        markup.add(inline_btn_1)
        await message.answer("Приветсвую Админ 🔑", reply_markup=markup)
    else:
        await message.answer('Вы не админ')


@dp.message_handler(commands=['dastan'])
async def accept(message: types.Message):
    data = requests.get(f'{host_url}api/v1/accountlist?tg={message.from_user.id}')
    # await message.delete()
    markup = InlineKeyboardMarkup(row_width=2)
    print(data)
    markup.add(InlineKeyboardButton('Принять ✅', callback_data=f'acceptapplication-{data["id"]}'))
    markup.add(InlineKeyboardButton('Отказ 🚫', callback_data=f'Ignore-{data["id"]}'))
    inline_btn_1 = InlineKeyboardButton('Домой', callback_data=f'home')
    markup.add(inline_btn_1)
    await message.answer(f'{data["account"]["username"]}, {data["account"]["username_tg"]}\n{data["course"]["title"]}',
                         reply_markup=markup)


@dp.message_handler()
async def accept(message: types.Message):
    print(message.text)
    if message.text == 'ZetRoom':
        await bot.send_photo(chat_id=message.chat.id, photo='https://sun3.userapi.com/sun3-13/s/v1/ig2/JO8lC-NB6LGn8px5ZRYrTEUkfPihlofSmu-NRSTxEAvrCIC7luwyRgkx2wMvVY6ixmWQREeInW-n9-2_rWM4F1An.jpg?size=1000x1000&quality=96&type=album')
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
        print(courses)
        print(call.message.caption)
        # print('Привет' not in call.message.text)
        if 'Привет' not in call.message.caption:
            await bot.delete_message(call.from_user.id, call.message.message_id)

        for i in courses:
            inline_btn_1 = InlineKeyboardButton(i['title'], callback_data=i['id'])
            markup.add(inline_btn_1)
        inline_btn_1 = InlineKeyboardButton('Домой', callback_data=f'home')
        markup.add(inline_btn_1)

        await bot.send_photo(chat_id=call.from_user.id, photo='https://sun3.userapi.com/sun3-11/s/v1/ig2/qXL0cHxu52gVZ4pTKbK-bx_TRSEzkfzQb7p5Gnl7btrf14iGtSsK4R5SCWTsXZhLEXlmAJhadoL_G1F1Y8JVKbeT.jpg?size=1920x1080&quality=96&type=album', caption='Здесь у нас все актуальные курсы, зайдя в них вы можете оставить заявки либо подробнее узнать о курсах 🌐', reply_markup=markup)
    if 'groups' in call.data:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        rer = requests.get(f'{host_url}api/v1/grouplistbot/?format=json').json()
        print(call.data)
        markup = InlineKeyboardMarkup()
        markup.clean()
        group = {}
        for i in rer:
            if str(i['id']) == call.data.split('-')[-1]:
                inline_btn_1 = InlineKeyboardButton(i['title'], callback_data=f'groupdetail-{i["id"]}')
                markup.add(inline_btn_1)
        inline_btn_1 = InlineKeyboardButton('Домой', callback_data=f'home')
        markup.add(inline_btn_1)
        await bot.send_message(chat_id=call.from_user.id, text='Группы', reply_markup=markup)
    if 'groupdetail' in call.data:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        rer = requests.get(f'{host_url}api/v1/grouplist/?format=json').json()
        markup = InlineKeyboardMarkup(row_width=2)
        for i in rer:
            if call.data.split('-')[-1] == str(i['id']):
                group = i
                break
        inline_btn_1 = InlineKeyboardButton('Разослать всем сообщение 🔑', callback_data=f'send_letter_group-{group["id"]}')
        markup.add(inline_btn_1)
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
        print(call.message.text)
        print('Привет' not in call.message.text)
        if 'Привет' not in call.message.text:
            await bot.delete_message(call.from_user.id, call.message.message_id)

        markup.clean()
        for i in meetings:
            inline_btn_1 = InlineKeyboardButton(i['title'], callback_data=f"meetdetail-{i['id']}")
            markup.add(inline_btn_1)
        inline_btn_1 = InlineKeyboardButton('Домой', callback_data=f'home')
        markup.add(inline_btn_1)
        await bot.send_message(chat_id=call.from_user.id, text='Здесь вы можете просмотреть актуальные ближайщие мероприятия\nНажав вы можете просмотреть детально, а также можете зписаться 🗓', reply_markup=markup)
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
    if call.data == 'home':
        await bot.delete_message(call.from_user.id, call.message.message_id)
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
        inline_btn_1 = InlineKeyboardButton('Домой', callback_data=f'home')
        markup.add(inline_btn_1)
        await bot.send_message(text='Заявки', chat_id=call.from_user.id, reply_markup=markup)
    if call.data == 'home':
        await call.message.delete()
        await send_welcome(message=call.message)
    if 'send_letter' in call.data:
        await rassylka_start(message=call.message)
            # await bot.send_message(text='Проверка', chat_id=call.from_user.id)
    elif 'student' in call.data:
        rer = requests.get(f'{host_url}api/v1/accountlist/?id={call.data.split("-")[-1]}').json()
        print(rer)
        markup = InlineKeyboardMarkup()
        inline_btn_1 = InlineKeyboardButton('Домой', callback_data=f'home')
        markup.add(inline_btn_1)
        if authadmin(call.from_user.id):
            inline_btn_1 = InlineKeyboardButton('Разослать сообщение', callback_data=f'send_letter_student-{rer[0]["id"]}')
            markup.add(inline_btn_1)
        if str(rer) != '[]':
            await bot.send_message(chat_id=call.from_user.id, text=rer, reply_markup=markup)


    if 'applicationfor' in call.data:
        rer = requests.get(f'{host_url}api/v1/applicationlist/').json()
        for i in rer:
            if str(i['id']) == str(call.data).split('-')[-1]:
                print(i)
                data = i
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('Принять ✅', callback_data=f'acceptapplication-{data["id"]}'))
                markup.add(InlineKeyboardButton('Отказ 🚫', callback_data=f'Ignore-{data["id"]}'))
                inline_btn_1 = InlineKeyboardButton('Домой', callback_data=f'home')
                markup.add(inline_btn_1)

                await bot.send_message(chat_id=call.from_user.id,
                    text=f'{data["account"]["username"]}, {data["account"]["username_tg"]}\n{data["course"]["title"]}',
                    reply_markup=markup)
                # await accept(message=call.message, data=i)
                break
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
        inline_btn_1 = InlineKeyboardButton('Домой', callback_data=f'home')
        markup.add(inline_btn_1)
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
            das = requests.post(url, json={"chat_id": application['account']["id"], "text": f"Вас успешно добавили в группу {group['title']}"})
            print(group)
            print(das)
            response = requests.request(method='PUT',
                                        url=f"{host_url}api/v1/groupupdate/{str(call.data.split('-')[-2])}", json=group)
            print(response.text)
            deler = requests.delete(f"{host_url}api/v1/applicationdelete/{application['id']}")
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
