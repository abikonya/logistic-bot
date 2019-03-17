from django.http import HttpResponse, HttpResponseServerError
import telebot
from . import config

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start"])
def command_start(message):
    bot.send_message(message.chat.id, "Bots webhook is working")


def index(request):
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
