from django.http import HttpResponse, HttpResponseServerError
import telebot
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
        print(request.headers)
        return ''
    else:
        raise HttpResponseServerError


@bot.message_handler(commands=["start"])
def command_start(message):
    bot.send_message(message.chat.id, "Bots webhook is working")
