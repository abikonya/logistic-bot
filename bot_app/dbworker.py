from .models import Products, Statuses, Payments
from . import api_func
from decimal import Decimal


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
    try:
        payment = Payments.objects.get(address=each.address)
        payment.amount = str(Decimal(each.total_received) / Decimal(100000000))
        payment.save(update_fields=['amount'])
    except Exception as err:
        new_payment = Payments(username=each.label,
                               address=each.address,
                               amount=each.total_received)
        new_payment.save()
