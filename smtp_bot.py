from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, Bot, executor, types
from dotenv import load_dotenv
from email.message import EmailMessage
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import smtplib, os, random
from config import token
import logging



from aiogram.dispatcher import FSMContext
from bs4 import BeautifulSoup

import requests
from config import token


bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

load_dotenv('.env')

num = random.randint(100000, 999999)
@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('мы отправили вам 6- значный код. введите этот код для подтверждения')
    print(num)
    

    def send_message(title: str, message: str, to_email: str) -> bool:
        sender = os.environ.get('smtp_email')
        password = os.environ.get('smtp_password')
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        try:
            server.login(sender, password)
            msg = EmailMessage()
            msg['Subject'] = title
            msg['From'] = sender
            msg['To'] = to_email
            msg.set_content(message)
            server.sendmail(sender, to_email, message)
            return True
        except Exception as error:
            return False
    print(send_message('code', str(num), 'asanalievurmat10@gmail.com'))

count = []
@dp.message_handler()
async def get(message:types.Message):
        if len(count) >= 3:
                await message.answer('Превышен количество попыток')

        elif message.text == str(num):
                await message.answer('Вы успешно зарегистрировались')
                
        elif message.text != str(num):
                count.append("Х")
                await message.answer('Неправильный код подтверждения')
                