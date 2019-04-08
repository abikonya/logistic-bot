from bot_app import api_func
import requests
import json
from bot_app.localization import Localization
from vedis import Vedis
from bot_app.tech_info import TechInfo

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


b = Localization()
TechInfo().set_language('test', 'ru')
language = TechInfo().return_language('test')
print(b.return_translation('rules_button', language))



def print_localization(name, lang):
    print(b.return_translation(name=name, language=lang))


print_localization('rules_button', 'ru')


print(b.return_all_translations('rules'))

