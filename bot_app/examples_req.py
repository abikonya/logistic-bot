from bot_app import api_func
import requests
import json
from bot_app import localization
from vedis import Vedis
from bot_app import tech_info
from logistic_bot import settings

# a = api_func.Api()
#
# a.set_user_id(telegram_id='test', user_id='D87hd487ft4')
# a.set_zipcode('test', 33815)
# print(a.return_param('test', 'user_id'))
# print(a.return_param('test', 'zipcode'))
#
# request = requests.get('https://strongbox.cc/?a=fnc.api.zip.getdistance&zip={zipcode}&tuser={user_id}'.format(
#                   zipcode=a.return_param('test', 'zipcode'),
#                   user_id=a.return_param('test', 'user_id')))
#
# print(json.loads(request.text))


tech_info.set_language('test', 'ru')
language = tech_info.return_language('test')
print(localization.return_translation('rules', language))


def print_localization(name, lang):
    print(localization.return_translation(name=name, language=lang))


print_localization('rules_button', 'ru')


print(localization.return_all_translations('rules'))
print(settings.BASE_DIR + r'\bot_app\localization.vdb')