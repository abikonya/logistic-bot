import re
import time

import telebot
from rest_framework.response import Response
from rest_framework.views import APIView
from telebot import types

from bot_app import api_func
from bot_app import config
from bot_app import localization
from bot_app import tech_info
from .models import AuthorizedCustomers
from .dbworker import add_product, status_updater
from bot_app.models import ConnectedApi

bot = telebot.TeleBot(config.token)


class UpdateBot(APIView):
    def post(self, request):
        json_string = request.body.decode("UTF-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])

        return Response({'code': 200})


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in AuthorizedCustomers.objects.values_list('telegram_id', flat=True):
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        button_en = types.InlineKeyboardButton(text='English', callback_data='en')
        button_ru = types.InlineKeyboardButton(text='Русский', callback_data='ru')
        keyboard.add(button_en, button_ru)
        bot.send_message(message.chat.id, 'Choose your language:\n\n Выберите Ваш язык:', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'You are not registered.\n\n Вы не зарегестрированы.', )


@bot.message_handler(commands=['zip'])
def enter_zip(message):
    tech_info.set_position(message.chat.id, 'zip')
    language = tech_info.return_language(message.chat.id)
    bot.send_message(message.chat.id, localization.return_translation('enter_zipcode', language))


@bot.message_handler(commands=['status'])
def status_check(message):
    language = tech_info.return_language(message.chat.id)
    tech_info.set_position(message.chat.id, 'status')
    bot.send_message(message.chat.id, localization.return_translation('enter_id', language))


@bot.callback_query_handler(func=lambda call: call.data in ['ru', 'en'])
def lang_select(call):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    if call.data == 'ru':
        tech_info.set_language(call.message.chat.id, call.data)
        language = tech_info.return_language(call.message.chat.id)
        button = types.KeyboardButton(text=localization.return_translation('rules_button', language))
        keyboard.add(button)
        bot.send_message(text=localization.return_translation('rules', language), chat_id=call.message.chat.id, reply_markup=keyboard)
    else:
        tech_info.set_language(call.message.chat.id, call.data)
        language = tech_info.return_language(call.message.chat.id)
        button = types.KeyboardButton(text=localization.return_translation('rules_button', language))
        keyboard.add(button)
        bot.send_message(text=localization.return_translation('rules', language), chat_id=call.message.chat.id, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in localization.return_all_translations('rules_button'))
@bot.message_handler(func=lambda message: message.text in localization.return_all_translations('success_button'))
def main(message):
    language = tech_info.return_language(message.chat.id)
    bot.send_message(message.chat.id, localization.return_translation('zip_searching', language) +
                     '\n\n' +
                     localization.return_translation('status_checking', language),
                     reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: re.search(r'^[0-9]+.+$', message.text))
def answer_on_digits(message):
    position = tech_info.return_position(message.chat.id)
    language = tech_info.return_language(message.chat.id)
    if position == 'zip':
        tech_info.set_position(message.chat.id, 'zip_listing')
        api_func.set_user_id(telegram_id=message.chat.id, user_id='D87hd487ft4')
        api_func.set_zipcode(telegram_id=message.chat.id, zipcode=message.text)
        get_distance = dict()
        for each in ConnectedApi.objects.all():
            get_distance = api_func.get_distance(message.chat.id, each)
        if type(get_distance) == dict and get_distance['address']:
            couriers_list = sorted(get_distance['address'], key=api_func.sort_by_dist)
            keyboard = types.InlineKeyboardMarkup()
            for each in couriers_list:
                button = types.InlineKeyboardButton(
                    text='{} {} {}'.format(each['zip'], each['distance'].replace("'", ''), each['name']), callback_data=each['zip'])
                keyboard.add(button)
            bot.send_message(message.chat.id, text=localization.return_translation('zip_list_choose', language), reply_markup=keyboard)
        elif not get_distance['address']:
            bot.send_message(message.chat.id, text=localization.return_translation('zip_not_found', language))
        elif type(get_distance) != dict:
            bot.send_message(message.chat.id, text=localization.return_translation('server_error', language))
    if position == 'status':
        tech_info.set_position(message.chat.id, 'status_checker')
        api_func.set_user_id(telegram_id=message.chat.id, user_id='D87hd487ft4')
        get_status = api_func.get_status()
        if type(get_status) == list and get_status:
            for each in get_status:
                status_updater(each)
                pack_id = each['pack_id']
                if pack_id == message.text:
                    bot.send_message(message.chat.id, text=localization.return_translation('status', language) + each['pack_id'])
                    if each['status'] == 'Confirm':
                        bot.send_message(message.chat.id, text=localization.return_translation('status_confirm', language))
                        api_func.set_pack_id(telegram_id=message.chat.id, pack_id=each['pack_id'])
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        button = types.KeyboardButton(text=localization.return_translation('enter_requisites_button', language))
                        keyboard.add(button)
                        bot.send_message(message.chat.id, text=localization.return_translation('enter_requisites', language))
                    elif each['status'] == 'Process':
                        bot.send_message(message.chat.id, text=localization.return_translation('status_process', language))
                    elif each['status'] == 'Rejected':
                        bot.send_message(message.chat.id, text=localization.return_translation('status_cancel', language))
                    elif each['status'] == 'Paid':
                        bot.send_message(message.chat.id,
                                         text=localization.return_translation('paid_status', language).format(
                                             each['summ'], each['date']))
        else:
            bot.send_message(message.chat.id, text='Нет такого заказа')
    elif position == 'store_name':
        tech_info.set_position(message.chat.id, 'store_phone')
        api_func.set_store_phone(telegram_id=message.chat.id, store_phone=message.text)
        bot.send_message(message.chat.id, text=localization.return_translation('order_number', language), reply_markup=types.ReplyKeyboardRemove())
    elif position == 'store_phone':
        tech_info.set_position(message.chat.id, 'order_number')
        api_func.set_order_number(telegram_id=message.chat.id, order_number=message.text)
        bot.send_message(message.chat.id, text=localization.return_translation('pickup_person', language))
    elif position == 'additional_info':
        tech_info.set_position(message.chat.id, 'price')
        api_func.set_price(telegram_id=message.chat.id, price=message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(text=localization.return_translation('send_button', language))
        keyboard.add(button)
        bot.send_message(message.chat.id, text=localization.return_translation('all_is_done', language), reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: re.search(r'^[0-9]+$', call.data))
def call_digit_answers(call):
    position = tech_info.return_position(call.message.chat.id)
    language = tech_info.return_language(call.message.chat.id)
    if position == 'zip_listing':
        api_func.set_zipcode(telegram_id=call.message.chat.id, zipcode=call.data)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button = types.KeyboardButton(text=localization.return_translation('zip_list_button', language))
        keyboard.add(button)
        bot.send_message(call.message.chat.id,
                         text=localization.return_translation('zip_list', language).format(
                             api_func.return_param(telegram_id=call.message.chat.id, param='zipcode')),
                         reply_markup=keyboard)
    elif position == 'choose_category':
        api_func.set_product_category(telegram_id=call.message.chat.id, product_category=call.data)
        keyboard = types.InlineKeyboardMarkup()
        get_items = api_func.get_items(call.message.chat.id)
        tech_info.set_position(call.message.chat.id, 'choose_item')
        for each in get_items['items_list']:
            button = types.InlineKeyboardButton(text='{}'.format(each['item_name']), callback_data=each['item_id'])
            keyboard.add(button)
        bot.send_message(call.message.chat.id, text=localization.return_translation('choose_item', language), reply_markup=keyboard)
    elif position == 'choose_item':
        api_func.set_product_item(call.message.chat.id, call.data)
        tech_info.set_position(call.message.chat.id, 'kind_of_pickup')
        keyboard = types.InlineKeyboardMarkup()
        button_shop = types.InlineKeyboardButton(text=localization.return_translation('shop_button', language), callback_data='shop')
        button_company = types.InlineKeyboardButton(text=localization.return_translation('company_button', language), callback_data='company')
        keyboard.add(button_shop, button_company)
        bot.send_message(call.message.chat.id, text=localization.return_translation('shop_or_company', language), reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['shop', 'company'])
def choose_kind(call):
    language = tech_info.return_language(call.message.chat.id)
    api_func.set_kind_of_pickup(call.message.chat.id, call.data)
    print(api_func.return_param(call.message.chat.id, 'kind_of_pickup'))
    tech_info.set_position(call.message.chat.id, 'enter_info')
    bot.send_message(call.message.chat.id, text=localization.return_translation('about_cargo', language))
    bot.send_message(call.message.chat.id, text=localization.return_translation('pickup_location', language))


@bot.message_handler(func=lambda message: message.text in localization.return_all_translations('zip_list_button'))
def show_stuff_list(message):
    tech_info.set_offset(message.chat.id, 1)
    offset = int(tech_info.return_offset(message.chat.id))
    language = tech_info.return_language(message.chat.id)
    tech_info.set_position(message.chat.id, 'stuff_list')
    get_stuff_list = api_func.get_all(telegram_id=message.chat.id, offset=offset)
    keyboard = types.InlineKeyboardMarkup()
    button_reset = types.InlineKeyboardButton(text=localization.return_translation('chosen_zip_reset', language), callback_data='reset')
    button_confirm = types.InlineKeyboardButton(text=localization.return_translation('chosen_zip_approve', language), callback_data='confirm')
    keyboard.add(button_reset, button_confirm)
    bot.send_message(message.chat.id, text=get_stuff_list['stuff_link'], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'confirm')
def courier_approved(call):
    language = tech_info.return_language(call.message.chat.id)
    tech_info.set_position(call.message.chat.id, 'choose_category')
    keyboard = types.InlineKeyboardMarkup()
    get_category = api_func.get_category(call.message.chat.id)
    for each in get_category['stuff_list']:
        button = types.InlineKeyboardButton(text='{}'.format(each['list_name']), callback_data=each['list_id'])
        keyboard.add(button)
    bot.send_message(call.message.chat.id, text=localization.return_translation('choose_category', language), reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'reset')
def courier_reset(call):
    language = tech_info.return_language(call.message.chat.id)
    tech_info.set_position(call.message.chat.id, 'zip_listing')
    get_distance = dict()
    for each in ConnectedApi.objects.all():
        get_distance = api_func.get_distance(call.message.chat.id, each)
    if type(get_distance) == dict and get_distance['address']:
        couriers_list = sorted(get_distance['address'], key=api_func.sort_by_dist)
        keyboard = types.InlineKeyboardMarkup()
        for each in couriers_list:
            button = types.InlineKeyboardButton(
                text='{} {} {}'.format(each['zip'], each['distance'].replace("'", ''), each['name']),
                callback_data=each['zip'])
            keyboard.add(button)
        bot.send_message(call.message.chat.id, text=localization.return_translation('zip_list_choose', language),
                         reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in localization.return_all_translations('send_button'))
def send_info(message):
    language = tech_info.return_language(message.chat.id)
    add_data = api_func.add_data(telegram_id=message.chat.id)
    api_func.set_task_id(message.chat.id, add_data['task_id'])
    add_product(message.chat.id)
    api_func.clear_all(message.chat.id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(localization.return_translation('success_button', language))
    keyboard.add(button)
    bot.send_message(message.chat.id, text=localization.return_translation('success', language) + add_data['task_id'], reply_markup=keyboard)


# Анкета. Profile


@bot.message_handler(func=lambda message: re.search(r'\w+', message.text))
def form(message):
    language = tech_info.return_language(message.chat.id)
    position = tech_info.return_position(message.chat.id)
    if position == 'status_checker':
        api_func.set_payout(telegram_id=message.chat.id, payout=message.text)
        payment_info = api_func.payment(message.chat.id)
        for each in payment_info['package_list']:
            if each['pack_id'] == api_func.return_param(message.chat.id, 'pack_id'):
                bot.send_message(message.chat.id,
                                 text=localization.return_translation('paid_status', language).format(each['summ'], each['date']))
    elif position == 'enter_info':
        tech_info.set_position(message.chat.id, 'pickup_location')
        api_func.set_pickup_location(telegram_id=message.chat.id, pickup_location=message.text)
        if api_func.return_param(message.chat.id, 'kind_of_pickup') == 'shop':
            bot.send_message(message.chat.id, text=localization.return_translation('store_name', language))
        else:
            bot.send_message(message.chat.id, text=localization.return_translation('company_name', language))
    elif position == 'pickup_location':
        if api_func.return_param(message.chat.id, 'kind_of_pickup') == 'shop':
            tech_info.set_position(message.chat.id, 'store_name')
            api_func.set_store_name(telegram_id=message.chat.id, store_name=message.text)
            bot.send_message(message.chat.id, text=localization.return_translation('store_phone', language))
        else:
            tech_info.set_position(message.chat.id, 'store_phone')
            api_func.set_store_name(telegram_id=message.chat.id, store_name=message.text)
            bot.send_message(message.chat.id, text=localization.return_translation('order_number', language))
    elif position == 'order_number':
        tech_info.set_position(message.chat.id, 'pickup_person')
        api_func.set_pickup_person(telegram_id=message.chat.id, pickup_person=message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(localization.return_translation('skip', language))
        keyboard.add(button)
        bot.send_message(message.chat.id, text=localization.return_translation('additional_info', language), reply_markup=keyboard)
    elif position == 'pickup_person':
        tech_info.set_position(message.chat.id, 'additional_info')
        if message.text in localization.return_all_translations('skip'):
            api_func.set_more_info(telegram_id=message.chat.id, more_info='')
            bot.send_message(message.chat.id, text=localization.return_translation('price', language), reply_markup=types.ReplyKeyboardRemove())
        else:
            api_func.set_more_info(telegram_id=message.chat.id, more_info=message.text)
            bot.send_message(message.chat.id, text=localization.return_translation('price', language), reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: message.text == '')
def empty_message(message):
    bot.send_message(message.chat.id, text='Пожалуйста введите запрашиваемую информацию')
