import re

import telebot
from rest_framework.response import Response
from rest_framework.views import APIView
from telebot import types

from bot_app import api_func
from bot_app import config
from bot_app import localization
from bot_app import tech_info

bot = telebot.TeleBot(config.token)


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


@bot.message_handler(func=lambda message: re.search(r'^[0-9]+$', message.text))
def answer_on_digits(message):
    position = tech_info.return_position(message.chat.id)
    language = tech_info.return_language(message.chat.id)
    if position == 'zip':
        tech_info.set_position(message.chat.id, 'zip_listing')
        api_func.set_user_id(telegram_id=message.chat.id, user_id='D87hd487ft4')
        api_func.set_zipcode(telegram_id=message.chat.id, zipcode=message.text)
        get_distance = api_func.get_distance(telegram_id=message.chat.id)
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
        api_func.set_user_id(telegram_id=message.chat.id, user_id=message.chat.id)
        get_status = api_func.get_status(telegram_id=message.chat.id)
        if type(get_status) == dict and get_status['package_list']:
            for each in get_status['package_list']:
                if each['pack_id'] == message.text:
                    bot.send_message(message.chat.id, text=localization.return_translation('status', language) + each['pack_id'])
                    if each['status'] == 'Conﬁrm':
                        api_func.set_pack_id(telegram_id=message.chat.id, pack_id=each['pack_id'])
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        button = types.KeyboardButton(text=localization.return_translation('enter_requisites_button', language))
                        keyboard.add(button)
                        bot.send_message(message.chat.id, text=localization.return_translation('enter_requisites', language),
                                         reply_markup=keyboard)
    elif position == 'store_name':
        tech_info.set_position(message.chat.id, 'store_phone')
        api_func.set_store_phone(telegram_id=message.chat.id, store_phone=message.text)
        bot.send_message(message.chat.id, text=localization.return_translation('order_number', language))
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


@bot.callback_query_handler(func=lambda call: re.search(r'^[0-9]{5}$', call.data))
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


@bot.message_handler(func=lambda message: message.text in localization.return_all_translations('zip_list_button'))
def show_stuff_list(message):
    tech_info.set_offset(message.chat.id, 1)
    offset = int(tech_info.return_offset(message.chat.id))
    language = tech_info.return_language(message.chat.id)
    tech_info.set_position(message.chat.id, 'stuff_list')
    get_stuff_list = api_func.get_all(telegram_id=message.chat.id, offset=offset)
    tech_info.set_pages(message.chat.id, int(get_stuff_list['pages']))
    pages = int(tech_info.return_pages(message.chat.id))
    if type(get_stuff_list) == dict and get_stuff_list['stuff_list']:
        keyboard = types.InlineKeyboardMarkup()
        button_next = types.InlineKeyboardButton(text='➡', callback_data='next')
        button_page = types.InlineKeyboardButton(text='стр {} из {}'.format(offset, pages), callback_data='None')
        button_prev = types.InlineKeyboardButton(text='⬅', callback_data='prev')
        button_confirm = types.InlineKeyboardButton(text=localization.return_translation('chosen_zip_approve', language),
                                                    callback_data='confirm')
        button_reset = types.InlineKeyboardButton(text=localization.return_translation('chosen_zip_reset', language),
                                                  callback_data='reset')
        keyboard.add(button_prev, button_page, button_next)
        keyboard.add(button_confirm, button_reset)
        text = str()
        for each in get_stuff_list['stuff_list']:
            text += '{}\n'.format(each['stuff_name'])
        bot.send_message(message.chat.id, text='Товар принимаемый курьером:\n', reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, text=text, reply_markup=keyboard, disable_web_page_preview=True)
    elif type(get_stuff_list) != dict:
        bot.send_message(message.chat.id, localization.return_translation('server_error', language))


@bot.callback_query_handler(func=lambda call: call.data == 'next')
def next_stuff_list(call):
    language = tech_info.return_language(call.message.chat.id)
    offset = int(tech_info.return_offset(call.message.chat.id))
    pages = int(tech_info.return_pages(call.message.chat.id))
    if offset < pages:
        tech_info.set_offset(call.message.chat.id, offset + 1)
    else:
        tech_info.set_offset(call.message.chat.id, 1)
    get_stuff_list = api_func.get_all(telegram_id=call.message.chat.id, offset=offset)
    if type(get_stuff_list) == dict and get_stuff_list['stuff_list']:
        keyboard = types.InlineKeyboardMarkup()
        button_next = types.InlineKeyboardButton(text='➡', callback_data='next')
        button_page = types.InlineKeyboardButton(text='стр {} из {}'.format(offset, pages), callback_data='None')
        button_prev = types.InlineKeyboardButton(text='⬅', callback_data='prev')
        button_confirm = types.InlineKeyboardButton(text=localization.return_translation('chosen_zip_approve', language),
                                                    callback_data='confirm')
        button_reset = types.InlineKeyboardButton(text=localization.return_translation('chosen_zip_reset', language),
                                                  callback_data='reset')
        keyboard.add(button_prev, button_page, button_next)
        keyboard.add(button_confirm, button_reset)
        text = str()
        for each in get_stuff_list['stuff_list']:
            text += '{}\n'.format(each['stuff_name'])
        bot.edit_message_text(text=text,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard,
                              disable_web_page_preview=True)
    elif type(get_stuff_list) != dict:
        bot.send_message(call.message.chat.id, localization.return_translation('server_error', language))


@bot.callback_query_handler(func=lambda call: call.data == 'prev')
def prev_stuff_list(call):
    language = tech_info.return_language(call.message.chat.id)
    offset = int(tech_info.return_offset(call.message.chat.id))
    pages = int(tech_info.return_pages(call.message.chat.id))
    if offset > 1:
        tech_info.set_offset(call.message.chat.id, offset - 1)
    else:
        tech_info.set_offset(call.message.chat.id, pages)
    get_stuff_list = api_func.get_all(telegram_id=call.message.chat.id, offset=offset)
    if type(get_stuff_list) == dict and get_stuff_list['stuff_list']:
        keyboard = types.InlineKeyboardMarkup()
        button_next = types.InlineKeyboardButton(text='➡', callback_data='next')
        button_page = types.InlineKeyboardButton(text='стр {} из {}'.format(offset, pages), callback_data='None')
        button_prev = types.InlineKeyboardButton(text='⬅', callback_data='prev')
        button_confirm = types.InlineKeyboardButton(text=localization.return_translation('chosen_zip_approve', language),
                                                    callback_data='confirm')
        button_reset = types.InlineKeyboardButton(text=localization.return_translation('chosen_zip_reset', language),
                                                  callback_data='reset')
        keyboard.add(button_prev, button_page, button_next)
        keyboard.add(button_confirm, button_reset)
        text = str()
        for each in get_stuff_list['stuff_list']:
            text += '{}\n'.format(each['stuff_name'])
        bot.edit_message_text(text=text,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard,
                              disable_web_page_preview=True)
    elif type(get_stuff_list) != dict:
        bot.send_message(call.message.chat.id, localization.return_translation('server_error', language))


@bot.callback_query_handler(func=lambda call: call.data in localization.return_all_translations('chosen_zip_approve'))
def courier_approved(call):
    language = tech_info.return_language(call.message.chat.id)
    tech_info.set_position(call.message.chat.id, 'enter_info')
    bot.send_message(call.message.chat.id, text=localization.return_translation('about_cargo', language),
                     reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(call.message.chat.id, text=localization.return_translation('pickup_location', language))


@bot.callback_query_handler(func=lambda call: call.data in localization.return_all_translations('chosen_zip_reset'))
def courier_reset(call):
    language = tech_info.return_language(call.message.chat.id)
    tech_info.set_position(call.message.chat.id, 'zip_listing')
    get_distance = api_func.get_distance(telegram_id=call.message.chat.id)
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


@bot.message_handler(func=lambda message: message.text == 'Отправить')
def send_info(message):
    language = tech_info.return_language(message.chat.id)
    add_data = api_func.add_data(telegram_id=message.chat.id)
    print(add_data)
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
    elif position == 'enter_info':
        tech_info.set_position(message.chat.id, 'pickup_location')
        api_func.set_pickup_location(telegram_id=message.chat.id, pickup_location=message.text)
        bot.send_message(message.chat.id, text=localization.return_translation('store_name', language))
    elif position == 'pickup_location':
        tech_info.set_position(message.chat.id, 'store_name')
        api_func.set_store_name(telegram_id=message.chat.id, store_name=message.text)
        bot.send_message(message.chat.id, text=localization.return_translation('store_phone', language))
    elif position == 'order_number':
        tech_info.set_position(message.chat.id, 'pickup_person')
        api_func.set_pickup_person(telegram_id=message.chat.id, pickup_person=message.text)
        bot.send_message(message.chat.id, text=localization.return_translation('additional_info', language))
    elif position == 'pickup_person':
        tech_info.set_position(message.chat.id, 'additional_info')
        api_func.set_more_info(telegram_id=message.chat.id, more_info=message.text)
        bot.send_message(message.chat.id, text=localization.return_translation('price', language))


@bot.message_handler(func=lambda message: message.text == '')
def empty_message(message):
    bot.send_message(message.chat.id, text='Пожалуйста введите запрашиваемую информацию')
