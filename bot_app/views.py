# from django.http import HttpResponse
import telebot
from . import config

bot = telebot.TeleBot(config.token)


def index(request):
    bot.process_new_updates(request)
