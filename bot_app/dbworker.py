from .models import Products, Statuses
from . import api_func


def add_product(telegram_id):
    query = Products(user_id=api_func.return_param(telegram_id, 'user_id'),
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


def status_updater(telegram_id, each):
    check = Statuses.objects.get(task_id=each['pack_id'])
    print(check)
    if Statuses.objects.get(task_id=each['pack_id']):
        status = Statuses.objects.get(task_id=each['pack_id'])
        status.status = each['status']
        status.save(update_fields=['status'])
    else:
        new_position = Statuses(user_id=telegram_id, task_id=each['pack_id'], status=each['status'])
        new_position.save()
