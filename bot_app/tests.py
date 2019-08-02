# from django.test import TestCase
#
# # Create your tests here.


import requests
import json


currency_url = 'https://blockchain.info/ticker'

currency = requests.get(currency_url)

currency_to_usd = json.loads(currency.text)['USD']

print(currency_to_usd)