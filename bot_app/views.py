import telebot
from telebot import types
import re
import json
from bot_app import config, localization
from bot_app import examples_req # не забыть удалить
from bot_app.api_func import Api, sort_by_dist
from rest_framework.response import Response
from rest_framework.views import APIView


bot = telebot.TeleBot(config.token)
api_instance = Api()
language = str()


class UpdateBot(APIView):
    def post(self, request):
        json_string = request.body.decode("UTF-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])

        return Response({'code': 200})


# Обработчики команд. Command's handlers


@bot.message_handler(commands=['start'])
def start(message):
    global api_instance
    api_instance.set_user_id(message.chat.id)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button_en = types.InlineKeyboardButton(text='English', callback_data='en')
    button_ru = types.InlineKeyboardButton(text='Русский', callback_data='ru')
    keyboard.add(button_en, button_ru)
    bot.send_message(message.chat.id, 'Choose your language:\n\n Выберите Ваш язык:', reply_markup=keyboard)


@bot.message_handler(commands=['zip'])
def enter_zip(message):
    global language
    bot.send_message(message.chat.id, localization.enter_zip[language])


@bot.message_handler(commands=['status'])
def status_check(message):
    bot.send_message(message.chat.id, localization.enter_id[language])


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
    bot.send_message(message.chat.id, localization.zip_searching[language] + '\n\n' + localization.status_check[language],
                     reply_markup=types.ReplyKeyboardRemove())


# Левая ветка. Left branch

@bot.message_handler(func=lambda message: re.search(r'^[0-9]{5}$', message.text))
def zip_list(message):
    global language, api_instance
    api_instance.set_zipcode(message.text)
    get_distance = api_instance.get_distance()
    print('Get distance --------------------------------- :\n', get_distance)
    couriers_list = sorted(get_distance['address'], key=sort_by_dist)
    print('Couriers list --------------------------------- :\n', couriers_list)
    keyboard = types.InlineKeyboardMarkup()
    for each in couriers_list:
        button = types.InlineKeyboardButton(text='{} {} {}'.format(each['zip'], each['distance'].replace("'", ''), each['name']),
                                            callback_data=each['zip'])
        keyboard.add(button)
    bot.send_message(message.chat.id, localization.zip_list_choose[language], reply_markup=keyboard)
