from aiogram import Bot, Dispatcher, types, executor
import os, smtplib
from logging import basicConfig, INFO
from dotenv import load_dotenv
import random 

load_dotenv(".env")
basicConfig(level=INFO)

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)

inline_buttons = [
    types.InlineKeyboardButton("Идентификация", callback_data='identification')
]

inline_keyboard = types.InlineKeyboardMarkup().add(*inline_buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f'добро пожаловать {message.from_user.first_name}', reply_markup=inline_keyboard)





@dp.callback_query_handler(lambda c: c.data == "identification")
async def start_verification(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Пожалуйста, введите вашу почту:")
    
@dp.message_handler(lambda message: not message.text.startswith('/'))
async def process_email(message: types.Message):
    verification_code = str(random.randint(100000, 999999))
    await send_verification_code(message.text, verification_code)
    await message.answer("Мы отправили вам 6-значный код. Пожалуйста, введите его:")

@dp.message_handler(lambda message: not message.text.startswith('/'))
async def process_code(message: types.Message):
    if message.text == verification_code:
        await message.answer("Вы успешно идентифицировались!")
    else:
        await message.answer("Неправильный ввод. Пожалуйста, введите код еще раз:")

def send_email(title, message, to_email):
    sender = os.environ.get('smtp_email')
    password = os.environ.get('smtp_password')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender, password)
        server.sendmail(sender, to_email, message)
        return "200 OK"
    except Exception as error:
        return f"Error: {error}"
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)