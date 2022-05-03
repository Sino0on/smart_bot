import requests

url = "https://api.telegram.org/bot5346235377:AAGg1mWc4FPRxGn1GFcnOBcj75MMLlrAJlA/sendMessage"

payload = {
    "text": "Меня зовут Бот",
    "chat_id": "889201663",
}

asd = {"username": "pop22", "password": "qwerty2003", "password2": "qwerty2003", "email": "asd@dsawe.da", "first_name": "yt", "last_name": "re", "tg": "795677145"}


headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.29.0",
    "Cookie": "csrftoken=XqYL4yFIf9Z7Ufe6nB6fg90TllF1OayZrJgebZFjjcdbY1q2rGVqiBIO7Ua82nD6",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}
response = requests.post('http://127.0.0.1:8000/api/v1/register/', json=asd, headers=headers)


print(response.text)