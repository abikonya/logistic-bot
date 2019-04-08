import telebot
from telebot import types
import re
from bot_app import config
from bot_app.localization import Localization
from bot_app.api_func import Api, sort_by_dist
from bot_app.tech_info import TechInfo
from rest_framework.response import Response
from rest_framework.views import APIView


bot = telebot.TeleBot(config.token)
api_instance = Api()
localization = Localization()


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
    TechInfo().set_position(message.chat.id, 'zip')
    language = TechInfo().return_language(message.chat.id)
    bot.send_message(message.chat.id, localization.return_translation('enter_zipcode', language))


@bot.message_handler(commands=['status'])
def status_check(message):
    language = TechInfo().return_language(message.chat.id)
    TechInfo().set_position(message.chat.id, 'status')
    bot.send_message(message.chat.id, localization.return_translation('enter_id', language))


# Выбор языка. Language select.


@bot.callback_query_handler(func=lambda call: call.data in ['ru', 'en'])
def lang_select(call):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    if call.data == 'ru':
        TechInfo().set_language(call.message.chat.id, call.data)
        language = TechInfo().return_language(call.message.chat.id)
        button = types.KeyboardButton(text=localization.return_translation('rules_button', language))
        keyboard.add(button)
        bot.send_message(text=localization.return_translation('rules', language), chat_id=call.message.chat.id, reply_markup=keyboard)
    else:
        TechInfo().set_language(call.message.chat.id, call.data)
        language = TechInfo().return_language(call.message.chat.id)
        button = types.KeyboardButton(text=localization.return_translation('rules_button', language))
        keyboard.add(button)
        bot.send_message(text=localization.return_translation('rules', language), chat_id=call.message.chat.id, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in localization.return_all_translations('rules_button'))
@bot.message_handler(func=lambda message: message.text in localization.return_all_translations('success_button'))
def main(message):
    language = TechInfo().return_language(message.chat.id)
    bot.send_message(message.chat.id, localization.return_translation('zip_searching', language) +
                     '\n\n' +
                     localization.return_translation('status_checking', language),
                     reply_markup=types.ReplyKeyboardRemove())


# Левая ветка. Left branch

@bot.message_handler(func=lambda message: re.search(r'^[0-9]{5}$', message.text))
def zip_listing(message):
    global api_instance
    language = TechInfo().return_language(message.chat.id)
    TechInfo().set_position(message.chat.id, 'zip_listing')
    api_instance.set_user_id(telegram_id=message.chat.id, user_id='D87hd487ft4')
    api_instance.set_zipcode(telegram_id=message.chat.id, zipcode=message.text)
    get_distance = api_instance.get_distance(telegram_id=message.chat.id)
    if type(get_distance) == dict and get_distance['address']:
        couriers_list = sorted(get_distance['address'], key=sort_by_dist)
        keyboard = types.InlineKeyboardMarkup()
        for each in couriers_list:
            button = types.InlineKeyboardButton(
                text='{} {} {}'.format(each['zip'], each['distance'].replace("'", ''), each['name']), callback_data=each['zip'])
            keyboard.add(button)
    elif not get_distance['address']:
        bot.send_message(message.chat.id, text=localization.return_translation('zip_not_found', language))
    elif type(get_distance) != dict:
        bot.send_message(message.chat.id, text=localization.return_translation('server_error', language))


@bot.callback_query_handler(func=lambda call: re.search(r'^[0-9]{5}$', call.data) or re.search(r'^[0-9]{4}$', call.data))
def call_data_answers(call):
    global api_instance
    position = TechInfo().return_language(call.message.chat.id)
    language = TechInfo().return_position(call.message.chat.id)
    if position == 'zip_listing':
        api_instance.set_zipcode(telegram_id=call.message.chat.id, zipcode=call.data)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button = types.KeyboardButton(text=localization.return_translation('zip_list_button', language))
        keyboard.add(button)
        bot.send_message(call.message.chat.id,
                         text=localization.return_translation('zip_list', language).format(
                             api_instance.return_param(telegram_id=call.message.chat.id, param='zipcode')),
                         reply_markup=keyboard)
    elif position == 'stuff_list':
        api_instance.set_product_item(telegram_id=call.message.chat.id, product_item=call.data)
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_confirm = types.KeyboardButton(text=localization.return_translation('chosen_zip_approve', language))
        button_reset = types.KeyboardButton(text=localization.return_translation('chosen_zip_reset', language))
        keyboard.add(button_confirm, button_reset)
        bot.send_message(call.message.chat.id, text='Вы выбрали {}'.format(api_instance.return_param(telegram_id=call.message.chat.id, param='product_item')),
                         reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in localization.return_all_translations('zip_list_button'))
def show_stuff_list(message):
    global api_instance
    TechInfo().set_offset(message.chat.id, 1)
    offset = TechInfo().return_offset(message.chat.id)
    language = TechInfo().return_language(message.chat.id)
    TechInfo().set_position(message.chat.id, 'stuff_list')
    get_stuff_list = api_instance.get_all(telegram_id=message.chat.id, offset=offset)
    TechInfo().set_pages(message.chat.id, int(get_stuff_list['pages']))
    pages = TechInfo().return_pages(message.chat.id)
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
        bot.send_message(message.chat.id, localization.return_translation('server_error', language))


@bot.callback_query_handler(func=lambda call: call.data == 'next')
def next_stuff_list(call):
    global api_instance
    language = TechInfo().return_language(call.message.chat.id)
    offset = TechInfo().return_offset(call.message.chat.id)
    pages = TechInfo().return_pages(call.message.chat.id)
    if offset < pages:
        offset = TechInfo().set_offset(call.message.chat.id, offset + 1)
    else:
        TechInfo().set_offset(call.message.chat.id, 1)
    get_stuff_list = api_instance.get_all(telegram_id=call.message.chat.id, offset=offset)
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
        bot.send_message(call.message.chat.id, localization.return_translation('server_error', language))


@bot.callback_query_handler(func=lambda call: call.data == 'prev')
def prev_stuff_list(call):
    global api_instance
    language = TechInfo().return_language(call.message.chat.id)
    offset = TechInfo().return_offset(call.message.chat.id)
    pages = TechInfo().return_pages(call.message.chat.id)
    if offset > 1:
        TechInfo().set_offset(call.message.chat.id, offset - 1)
    else:
        TechInfo().set_offset(call.message.chat.id, pages)
    get_stuff_list = api_instance.get_all(telegram_id=call.message.chat.id, offset=offset)
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
        bot.answer_callback_query(callback_query_id='prev')
    elif type(get_stuff_list) != dict:
        bot.send_message(call.message.chat.id, localization.return_translation('server_error', language))


@bot.message_handler(func=lambda message: message.text == 'Принять')
def enter_info(message):
    language = TechInfo().return_language(message.chat.id)
    TechInfo().set_position(message.chat.id, 'enter_info')
    bot.send_message(message.chat.id, text=localization.return_translation('about_cargo', language))
    bot.send_message(message.chat.id, text=localization.return_translation('pickup_location', language))


@bot.message_handler(func=lambda message: message.text == 'Отправить')
def send_info(message):
    global api_instance
    language = TechInfo().return_language(message.chat.id)
    add_data = api_instance.add_data(telegram_id=message.chat.id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.ReplyKeyboardMarkup(localization.return_translation('success_button', language))
    keyboard.add(button)
    bot.send_message(message.chat.id, text=localization.return_translation('success', language) + add_data['task_id'], reply_markup=keyboard)


# Правая ветка. Right branch


@bot.message_handler(func=lambda message: re.search(r'^[0-9]', message.text))
def status_checker(message):
    global api_instance
    language = TechInfo().return_language(message.chat.id)
    TechInfo().set_position(message.chat.id, 'status_checker')
    api_instance.set_user_id(telegram_id=message.chat.id, user_id=message.chat.id)
    get_status = api_instance.get_status(telegram_id=message.chat.id)
    if type(get_status) == dict and get_status['package_list']:
        for each in get_status['package_list']:
            if each['pack_id'] == message.text:
                bot.send_message(message.chat.id, text=localization.return_translation('status', language) + each['pack_id'])
                if each['status'] == 'Conﬁrm':
                    api_instance.set_pack_id(telegram_id=message.chat.id, pack_id=each['pack_id'])
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    button = types.KeyboardButton(text=localization.return_translation('enter_requisites_button', language))
                    keyboard.add(button)
                    bot.send_message(message.chat.id, text=localization.return_translation('enter_requisites', language),
                                     reply_markup=keyboard)


# Анкета. Profile


@bot.message_handler(func=lambda message: re.search(r'\w+', message.text))
def form(message):
    global api_instance
    language = TechInfo().return_language(message.chat.id)
    position = TechInfo().return_position(message.chat.id)
    if position == 'status_checker':
        api_instance.set_payout(telegram_id=message.chat.id, payout=message.text)
    elif position == 'enter_info':
        TechInfo().set_position(message.chat.id, 'pickup_location')
        api_instance.set_pickup_location(telegram_id=message.chat.id, pickup_location=message.text)
        bot.send_message(message.chat.id, text=localization.return_translation('store_name', language), reply_markup=types.ReplyKeyboardRemove)
    elif position == 'pickup_location':
        TechInfo().set_position(message.chat.id, 'store_name')
        api_instance.set_store_name(telegram_id=message.chat.id, store_name=message.text)
        bot.send_message(message.chat.id, text=localization.return_translation('store_phone', language))
    elif position == 'store_name':
        TechInfo().set_position(message.chat.id, 'store_phone')
        api_instance.set_store_phone(telegram_id=message.chat.id, store_phone=message.text)
        bot.send_message(message.chat.id, text=localization.return_translation('order_number', language))
    elif position == 'store_phone':
        TechInfo().set_position(message.chat.id, 'order_number')
        api_instance.set_order_number(telegram_id=message.chat.id, order_number=message.text)
        bot.send_message(message.chat.id, text=localization.return_translation('pickup_person', language))
    elif position == 'order_number':
        TechInfo().set_position(message.chat.id, 'pickup_person')
        api_instance.set_pickup_person(telegram_id=message.chat.id, pickup_person=message.text)
        bot.send_message(message.chat.id, text=localization.return_translation('additional_info', language))
    elif position == 'pickup_person':
        TechInfo().set_position(message.chat.id, 'additional_info')
        api_instance.set_more_info(telegram_id=message.chat.id, more_info=message.text)
        bot.send_message(message.text.id, text=localization.return_translation('product_name', language))
    elif position == 'additional_info':
        TechInfo().set_position(message.chat.id, 'product_name')
        api_instance.set_product_item(telegram_id=message.chat.id, product_item=message.text)
        bot.send_message(message.text.id, text=localization.return_translation('price', language))
    elif position == 'product_name':
        api_instance.set_price(telegram_id=message.chat.id, price=message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(text=localization.return_translation('send_button', language))
        keyboard.add(button)
        bot.send_message(message.chat.id, text=localization.return_translation('all_is_done', language), reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == '')
def empty_message(message):
    bot.send_message(message.chat.id, text='Пожалуйста введите запрашиваемую информацию')
