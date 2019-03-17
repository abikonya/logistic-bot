from django.http import HttpResponse, HttpResponseServerError
import telebot
from telebot import types
from . import config

bot = telebot.TeleBot(config.token)


def index(request):
    if 'content-length' in request.headers and 'content-type' in request.headers \
            and request.headers['content-type'] == 'application/json':
        length = int(request.headers['content-length'])
        json_string = request.body.read(length)
        json_string = json_string.decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        if update.message:
            bot.process_new_messages([update.message])
        if update.inline_query:
            bot.process_new_inline_query([update.inline_query])
        print(request)
        return ''
    else:
        raise HttpResponseServerError


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global position
    position = 'send_welcome'
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id,
                     'Добро пожаловать в BotsApp 😊 \n'
                     'Для авторизации нажмите кнопку «Отправить мой номер».',
                     reply_markup=keyboard)
