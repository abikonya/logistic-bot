from .models import Products, Statuses, Payments
from . import api_func
import requests
import json
import math

currency_url = 'https://blockchain.info/ticker'

currency = requests.get(currency_url)

currency_to_usd = json.loads(currency.text)['USD']


def add_product(telegram_id):
    query = Products(api=api_func.return_param(telegram_id, 'api_address'),
                     telegram_id=telegram_id,
                     user_id=api_func.return_param(telegram_id, 'user_id'),
                     task_id=api_func.return_param(telegram_id, 'task_id'),
                     zipcode=api_func.return_param(telegram_id, 'zipcode'),
                     store_name=api_func.return_param(telegram_id, 'store_name'),
                     store_phone=api_func.return_param(telegram_id, 'store_phone'),
                     order_number=api_func.return_param(telegram_id, 'order_number'),
                     pickup_person=api_func.return_param(telegram_id, 'pickup_person'),
                     pickup_location=api_func.return_param(telegram_id, 'pickup_location'),
                     more_info=api_func.return_param(telegram_id, 'more_info'),
                     product_category=api_func.return_param(telegram_id, 'product_category'),
                     product_item=api_func.return_param(telegram_id, 'product_item'),
                     price=api_func.return_param(telegram_id, 'price'))
    query.save()


def status_updater(each):
    try:
        status = Statuses.objects.get(task_id=each['pack_id'])
        status.status = each['status']
        status.save(update_fields=['status'])
    except Exception:
        new_position = Statuses(api=each['api'],
                                task_id=each['pack_id'],
                                status=each['status'])
        new_position.save()


def payments_updater(each):
    if each.total_received is True and each.total_received > 0:
        total = math.ceil((each.total_received / 100000000) * currency_to_usd['buy'])
        obj, created = Payments.objects.update_or_create(
            username=each.label,
            address=each.address,
            amount=total)
