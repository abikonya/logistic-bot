from .models import Products
from . import api_func


def add_product(telegram_id):
    Products.user_id = api_func.return_param(telegram_id, 'user_id')
    Products.zipcode = api_func.return_param(telegram_id, 'zipcode')
    Products.store_name = api_func.return_param(telegram_id, 'store_name')
    Products.store_phone = api_func.return_param(telegram_id, 'store_phone')
    Products.order_number = api_func.return_param(telegram_id, 'order_number')
    Products.pickup_person = api_func.return_param(telegram_id, 'pickup_person')
    Products.pickup_location = api_func.return_param(telegram_id, 'pickup_location')
    Products.more_info = api_func.return_param(telegram_id, 'more_info')
    Products.product_category = api_func.return_param(telegram_id, 'product_category')
    Products.product_item = api_func.return_param(telegram_id, 'product_item')
    Products.price = api_func.return_param(telegram_id, 'price')