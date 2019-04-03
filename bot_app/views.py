import telebot
from telebot import types
import re
from bot_app import config
from bot_app.localization import *
from bot_app.api_func import Api, sort_by_dist
from rest_framework.response import Response
from rest_framework.views import APIView


bot = telebot.TeleBot(config.token)
api_instance = Api()
language = str()
position = str()
offset = int()
pages = int()


class UpdateBot(APIView):
    def post(self, request):
        json_string = request.body.decode("UTF-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])

        return Response({'code': 200})


# Обработчики команд. Command's handlers


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button_en = types.InlineKeyboardButton(text='English', callback_data='en')
    button_ru = types.InlineKeyboardButton(text='Русский', callback_data='ru')
    keyboard.add(button_en, button_ru)
    bot.send_message(message.chat.id, 'Choose your language:\n\n Выберите Ваш язык:', reply_markup=keyboard)


@bot.message_handler(commands=['zip'])
def enter_zip(message):
    global language, position
    position = 'zip'
    bot.send_message(message.chat.id, enter_zipcode[language])


@bot.message_handler(commands=['status'])
def status_check(message):
    global position, language
    position = 'status'
    bot.send_message(message.chat.id, enter_id[language])


# Выбор языка. Language select.


@bot.callback_query_handler(func=lambda call: call.data in ['ru', 'en'])
def lang_select(call):
    global language
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    if call.data == 'ru':
        language = 'ru'
        button = types.KeyboardButton(text=rules_button[language])
        keyboard.add(button)
        bot.send_message(text=rules[language], chat_id=call.message.chat.id, reply_markup=keyboard)
    else:
        language = 'en'
        button = types.KeyboardButton(text=rules_button[language])
        keyboard.add(button)
        bot.send_message(text=rules[language], chat_id=call.message.chat.id, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == rules_button[language])
@bot.message_handler(func=lambda message: message.text == success_button[language])
def main(message):
    global language
    bot.send_message(message.chat.id, zip_searching[language] + '\n\n' + status_checking[language],
                     reply_markup=types.ReplyKeyboardRemove())


# Левая ветка. Left branch

@bot.message_handler(func=lambda message: re.search(r'^[0-9]{5}$', message.text))
def zip_listing(message):
    global language, api_instance, position
    position = 'zip_listing'
    api_instance.set_user_id('D87hd487ft4')
    api_instance.set_zipcode(message.text)
    get_distance = api_instance.get_distance()
    if type(get_distance) == dict and get_distance['address']:
        couriers_list = sorted(get_distance['address'], key=sort_by_dist)
        keyboard = types.InlineKeyboardMarkup()
        for each in couriers_list:
            button = types.InlineKeyboardButton(
                text='{} {} {}'.format(each['zip'], each['distance'].replace("'", ''), each['name']), callback_data=each['zip'])
            keyboard.add(button)
            bot.send_message(message.chat.id, zip_list_choose[language], reply_markup=keyboard)
    elif not get_distance['address']:
        bot.send_message(message.chat.id, text=zip_not_found[language])
    elif type(get_distance) != dict:
        bot.send_message(message.chat.id, text=server_error[language])


@bot.callback_query_handler(func=lambda call: re.search(r'^[0-9]{5}$', call.data))
def call_data_answers(call):
    global language, api_instance, position
    if position == 'zip_listing':
        api_instance.set_zipcode(call.data)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button = types.KeyboardButton(text=zip_list_button[language])
        keyboard.add(button)
        bot.send_message(call.message.chat.id, text=zip_list[language].format(api_instance.return_zipcode()),
                         reply_markup=keyboard)
    elif position == 'stuff_list':
        global language, api_instance
        api_instance.set_product_item(call.data)
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_confirm = types.KeyboardButton(text=chosen_zip_approve)
        button_reset = types.KeyboardButton(text=chosen_zip_reset)
        keyboard.add(button_confirm, button_reset)
        bot.send_message(call.message.chat.id, text='Вы выбрали {}'.format(call.data), reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == zip_list_button[language])
def show_stuff_list(message):
    global language, position, api_instance
    global offset, pages
    position = 'stuff_list'
    offset = 1
    get_stuff_list = api_instance.get_all(offset)
    pages = int(get_stuff_list['pages'])
    if type(get_stuff_list) == dict and get_stuff_list['stuff_list']:
        keyboard = types.InlineKeyboardMarkup()
        button_next = types.InlineKeyboardButton(text='➡', callback_data='next')
        button_prev = types.InlineKeyboardButton(text='⬅', callback_data='prev')
        for each in get_stuff_list['stuff_list']:
            button = types.InlineKeyboardButton(
                text='{} {}'.format(each['id'], each['stuff_name']), callback_data=each['id'])
            keyboard.add(button)
        keyboard.add(button_prev, button_next)
        bot.send_message(message.chat.id, text='Выберите товар, который хотите отправить.\n '
                                               'Товар принимаемый курьером:\n стр {} из {}'.format(offset, pages),
                         reply_markup=keyboard)
    elif type(get_stuff_list) != dict:
        bot.send_message(message.chat.id, server_error[language])


@bot.callback_query_handler(func=lambda call: call.data == 'next')
def next_stuff_list(call):
    global api_instance, language
    global offset, pages
    if offset < pages:
        offset += 1
    else:
        offset = 1
    get_stuff_list = api_instance.get_all(offset)
    if type(get_stuff_list) == dict and get_stuff_list['stuff_list']:
        keyboard = types.InlineKeyboardMarkup()
        button_next = types.InlineKeyboardButton(text='➡', callback_data='next')
        button_prev = types.InlineKeyboardButton(text='⬅', callback_data='prev')
        for each in get_stuff_list['stuff_list']:
            button = types.InlineKeyboardButton(
                text='{} {}'.format(each['id'], each['stuff_name']), callback_data=each['id'])
            keyboard.add(button)
        keyboard.add(button_prev, button_next)
        bot.edit_message_text(text='Выберите товар, который хотите отправить.\n '
                                   'Товар принимаемый курьером:\n стр {} из {}'.format(offset, pages),
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard)
    elif type(get_stuff_list) != dict:
        bot.send_message(call.message.chat.id, server_error[language])


@bot.callback_query_handler(func=lambda call: call.data == 'prev')
def prev_stuff_list(call):
    global api_instance, language
    global offset, pages
    if offset > 1:
        offset -= 1
    else:
        offset = pages
    get_stuff_list = api_instance.get_all(offset)
    if type(get_stuff_list) == dict and get_stuff_list['stuff_list']:
        keyboard = types.InlineKeyboardMarkup()
        button_next = types.InlineKeyboardButton(text='➡', callback_data='next')
        button_prev = types.InlineKeyboardButton(text='⬅', callback_data='prev')
        for each in get_stuff_list['stuff_list']:
            button = types.InlineKeyboardButton(
                text='{} {}'.format(each['id'], each['stuff_name']), callback_data=each['id'])
            keyboard.add(button)
        keyboard.add(button_prev, button_next)
        bot.edit_message_text(text='Выберите товар, который хотите отправить.\n '
                                   'Товар принимаемый курьером:\n стр {} из {}'.format(offset, pages),
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard)
    elif type(get_stuff_list) != dict:
        bot.send_message(call.message.chat.id, server_error[language])


@bot.message_handler(func=lambda message: message.text == 'Принять')
def enter_info(message):
    global language, position
    position = 'enter_info'
    bot.send_message(message.chat.id, text=about_cargo[language])
    bot.send_message(message.chat.id, text=pickup_location[language])


@bot.message_handler(func=lambda message: message.text == 'Отправить')
def send_info(message):
    global api_instance, language
    add_info = api_instance.add_info()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.ReplyKeyboardMarkup(success_button[language])
    keyboard.add(button)
    bot.send_message(message.chat.id, text=success[language] + add_info['task_id'], reply_markup=keyboard)


# Правая ветка. Right branch


@bot.message_handler(func=lambda message: re.search(r'^[0-9]', message.text))
def status_checker(message):
    global api_instance, language, position
    position = 'status_checker'
    user_id = api_instance.set_user_id(message.chat.id)
    get_status = api_instance.get_status()
    if type(get_status) == dict and get_status['package_list']:
        for each in get_status['package_list']:
            if each['pack_id'] == message.text:
                bot.send_message(message.chat.id, text=status[language] + each['pack_id'])
                if each['status'] == 'Conﬁrm':
                    api_instance.set_pack_id(each['pack_id'])
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    button = types.KeyboardButton(text=enter_requisites_button[language])
                    keyboard.add(button)
                    bot.send_message(message.chat.id, text=enter_requisites[language], reply_markup=keyboard)


@bot.message_handler(func=lambda message: re.search(r'\w+', message.text))
def payment(message):
    global position, api_instance, language
    if position == 'status_checker':
        api_instance.payment(message.text)


# Анкета. Profile


@bot.message_handler(func=lambda message: re.search(r'\w+', message.text))
def form(message):
    global position, api_instance
    if position == 'enter_info':
        position = 'pickup_location'
        api_instance.set_pickup_location(message.text)
        bot.send_message(message.chat.id, text=store_name[language], reply_markup=types.ReplyKeyboardRemove)
    elif position == 'pickup_location':
        position = 'store_name'
        api_instance.set_store_name(message.text)
        bot.send_message(message.chat.id, text=store_phone[language])
    elif position == 'store_name':
        position = 'store_phone'
        api_instance.set_store_phone(message.text)
        bot.send_message(message.chat.id, text=order_number[language])
    elif position == 'store_phone':
        position = 'order_number'
        api_instance.set_order_number(message.text)
        bot.send_message(message.chat.id, text=pickup_person[language])
    elif position == 'order_number':
        position = 'pickup_person'
        api_instance.set_pickup_person(message.text)
        bot.send_message(message.chat.id, text=additional_info[language])
    elif position == 'pickup_person':
        position = 'additional_info'
        api_instance.set_additional_info(message.text)
        bot.send_message(message.text.id, text=product_name[language])
    elif position == 'additional_info':
        position = 'product_name'
        api_instance.set_product_name(message.text)
        bot.send_message(message.text.id, text=price[language])
    elif position == 'product_name':
        api_instance.set_price(message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(text=send_button[language])
        keyboard.add(button)
        bot.send_message(message.chat.id, text=all_is_done[language], reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == '')
def empty_message(message):
    bot.send_message(message.chat.id, text='Пожалуйста введите запрашиваемую информацию')
