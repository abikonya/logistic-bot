import telebot
from telebot import types
import re
from . import config, api_functions, localization
from rest_framework.response import Response
from rest_framework.views import APIView


bot = telebot.TeleBot(config.token)
language = str()


class UpdateBot(APIView):
    def post(self, request):
        json_string = request.body.decode("UTF-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])

        return Response({'code': 200})


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button_en = types.InlineKeyboardButton(text='English', callback_data='en')
    button_ru = types.InlineKeyboardButton(text='Русский', callback_data='ru')
    keyboard.add(button_en, button_ru)
    bot.send_message(message.chat.id, 'Choose your language:\n\n Выберите Ваш язык:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['ru', 'en'])
def lang_select(call):
    global language
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    if call.data == 'ru':
        language = 'ru'
        button = types.KeyboardButton(text=localization.rules_button[language])
        keyboard.add(button)
        bot.send_message(text=localization.rules[language], chat_id=call.message.chat.id, reply_markup=keyboard)
    else:
        language = 'en'
        button = types.KeyboardButton(text=localization.rules_button[language])
        keyboard.add(button)
        bot.send_message(text=localization.rules[language], chat_id=call.message.chat.id, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == localization.rules_button[language])
def main(message):
    global language
    bot.send_message(message.chat.id, localization.zip_searching[language] + localization.status_check[language],
                     reply_markup=types.ReplyKeyboardRemove())


