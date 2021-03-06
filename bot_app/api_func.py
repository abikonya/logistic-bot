import requests
import json
from vedis import Vedis
import os
from bot_app.models import ConnectedApi

base_dir = os.path.dirname(os.path.abspath(__file__))
os.path.join(base_dir, 'accounts_info.vdb')


def set_api_address(telegram_id, api_address, get_distance, get_all, add_data, get_category, get_items, get_status, payment):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['api_address'] = api_address
            account['get_distance'] = get_distance
            account['get_all'] = get_all
            account['add_data'] = add_data
            account['get_category'] = get_category
            account['get_items'] = get_items
            account['get_status'] = get_status
            account['payment'] = payment
        except Exception as err:
            print(err)


def set_user_id(telegram_id, user_id):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['user_id'] = user_id
        except Exception as err:
            print(err)


def set_zipcode(telegram_id, zipcode):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['zipcode'] = zipcode
        except Exception as err:
            print(err)


def set_store_name(telegram_id, store_name):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['store_name'] = store_name
        except Exception as err:
            print(err)


def set_store_phone(telegram_id, store_phone):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['store_phone'] = store_phone
        except Exception as err:
            print(err)


def set_order_number(telegram_id, order_number):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['order_number'] = order_number
        except Exception as err:
            print(err)


def set_pickup_person(telegram_id, pickup_person):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['pickup_person'] = pickup_person
        except Exception as err:
            print(err)


def set_pickup_location(telegram_id, pickup_location):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['pickup_location'] = pickup_location
        except Exception as err:
            print(err)


def set_more_info(telegram_id, more_info):
    with Vedis(os.path.join(base_dir, os.path.join(base_dir, 'accounts_info.vdb'))) as db:
        try:
            account = db.Hash(telegram_id)
            account['more_info'] = more_info
        except Exception as err:
            print(err)


def set_product_category(telegram_id, product_category):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['product_category'] = product_category
        except Exception as err:
            print(err)


def set_product_item(telegram_id, product_item):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['product_item'] = product_item
        except Exception as err:
            print(err)


def set_price(telegram_id, price):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['price'] = price
        except Exception as err:
            print(err)


def set_pack_id(telegram_id, pack_id):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['pack_id'] = pack_id
        except Exception as err:
            print(err)


def set_payout(telegram_id, payout):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['payout'] = payout
        except Exception as err:
            print(err)


def set_list_id(telegram_id, list_id):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['list_id'] = list_id
        except Exception as err:
            print(err)


def set_kind_of_pickup(telegram_id, kind_of_pickup):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['kind_of_pickup'] = kind_of_pickup
        except Exception as err:
            print(err)


def set_task_id(telegram_id, task_id):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['task_id'] = task_id
        except Exception as err:
            print(err)


def return_param(telegram_id, param):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            return account[param].decode('UTF-8')
        except Exception as err:
            print(err)


def clear_all(telegram_id):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            account['zipcode'] = ''
            account['store_name'] = ''
            account['store_phone'] = ''
            account['order_number'] = ''
            account['pickup_person'] = ''
            account['pickup_location'] = ''
            account['more_info'] = ''
            account['product_category'] = ''
            account['product_item'] = ''
            account['price'] = ''
        except Exception as err:
            print(err)


def get_distance(telegram_id, args):
    try:
        request = requests.get((args.address + args.get_distance).format(
            zipcode=return_param(telegram_id, 'zipcode'),
            user_id=return_param(telegram_id, 'user_id')))
        answer = json.loads(request.text)
        if answer['address']:
            set_api_address(telegram_id=telegram_id,
                            api_address=args.address,
                            get_distance=args.get_distance,
                            get_all=args.get_all,
                            add_data=args.add_data,
                            get_category=args.get_category,
                            get_items=args.get_items,
                            get_status=args.get_status,
                            payment=args.payment
                            )
            return answer
    except Exception as err:
        print(err)


def get_all(telegram_id, offset):
    try:
        url = (return_param(telegram_id, 'api_address') + return_param(telegram_id, 'get_all'))
        request = requests.get(url.format(
            user_id=return_param(telegram_id, 'user_id'),
            zipcode=return_param(telegram_id, 'zipcode'),
            offset=offset))
        return json.loads(request.text)
    except Exception as err:
        print(err)


def add_data(telegram_id):
    try:
        url = (return_param(telegram_id, 'api_address') + return_param(telegram_id, 'add_data'))
        request = requests.get(url.format(user_id=return_param(telegram_id, 'user_id'),
                                                                          zipcode=return_param(telegram_id, 'zipcode'),
                                                                          store_name=return_param(telegram_id, 'store_name'),
                                                                          store_phone=return_param(telegram_id, 'store_phone'),
                                                                          order_number=return_param(telegram_id, 'order_number'),
                                                                          pickup_person=return_param(telegram_id, 'pickup_person'),
                                                                          pickup_location=return_param(telegram_id, 'pickup_location'),
                                                                          more_info=return_param(telegram_id, 'more_info'),
                                                                          product_category=return_param(telegram_id, 'product_category'),
                                                                          product_item=return_param(telegram_id, 'product_item'),
                                                                          price=return_param(telegram_id, 'price')))
        return json.loads(request.text)
    except Exception as err:
        print(err)


def get_category(telegram_id):
    try:
        url = (return_param(telegram_id, 'api_address') + return_param(telegram_id, 'get_category'))
        request = requests.get(url.format(
            user_id=return_param(telegram_id, 'user_id'),
            zipcode=return_param(telegram_id, 'zipcode')))
        return json.loads(request.text)
    except Exception as err:
        print(err)


def get_items(telegram_id):
    try:
        url = (return_param(telegram_id, 'api_address') + return_param(telegram_id, 'get_items'))
        request = requests.get(url.format(
            user_id=return_param(telegram_id, 'user_id'),
            zipcode=return_param(telegram_id, 'zipcode'),
            list_id=return_param(telegram_id, 'product_category')))
        return json.loads(request.text)
    except Exception as err:
        print(err)


def get_status():
    try:
        all_statuses = list()
        for each in ConnectedApi.objects.all():
            url = each.address + each.get_status
            request = requests.get(url.format(
                user_id='D87hd487ft4'))
            answer = json.loads(request.text)['package_list']
            for every in answer:
                every['api'] = each.address
                all_statuses.append(every)
        return all_statuses
    except Exception as err:
        print(err)


def payment(telegram_id):
    try:
        url = (return_param(telegram_id, 'api_address') + return_param(telegram_id, 'payment'))
        request = requests.get(url.format(
            user_id=return_param(telegram_id, 'user_id'),
            pack_id=return_param(telegram_id, 'pack_id'),
            payout=return_param(telegram_id, 'payout')))
        return json.loads(request.text)
    except Exception as err:
        print(err)


def sort_by_dist(response):
    return response['distance'].replace("'", '')
