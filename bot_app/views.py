from django.http import HttpResponse
import telebot
from . import config

bot = telebot.TeleBot(config.token)
bot.set_webhook(url=config.bots_site)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, 'Bot is working')


def index(request):
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return 'ok', 200
