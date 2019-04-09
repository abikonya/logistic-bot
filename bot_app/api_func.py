import requests
import json
from vedis import Vedis
import os


base_dir = os.path.dirname(os.path.abspath(__file__))
os.path.join(base_dir, 'accounts_info.vdb')


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


def return_param(telegram_id, param):
    with Vedis(os.path.join(base_dir, 'accounts_info.vdb')) as db:
        try:
            account = db.Hash(telegram_id)
            return account[param].decode('UTF-8')
        except Exception as err:
            print(err)


def get_distance(telegram_id):
    try:
        request = requests.get('https://strongbox.cc/?a=fnc.api.zip.getdistance&zip={zipcode}&tuser={user_id}'.format(
            zipcode=return_param(telegram_id, 'zipcode'),
            user_id=return_param(telegram_id, 'user_id')))
        return json.loads(request.text)
    except Exception as err:
        print(err)


def get_all(telegram_id, offset):
    try:
        request = requests.get('https://strongbox.cc/?a=fnc.api.list.getall&tuser={user_id}&zip={zipcode}&count=10&offset={offset}'.format(
            user_id=return_param(telegram_id, 'user_id'),
            zipcode=return_param(telegram_id, 'zipcode'),
            offset=offset))
        return json.loads(request.text)
    except Exception as err:
        print(err)


def add_data(telegram_id):
    try:
        request = requests.get('https://strongbox.cc/?a=fnc.api.package.add&tuser={user_id}&zip={zipcode}&store_name={store_name}'
                                '&store_phone={store_phone}&order_number={order_number}&pickup_person={pickup_person}'
                                '&pickup_location={pickup_location}&more_information={more_info}'
                                '&product_item={product_item}&product_price={price}'.format(user_id=return_param(telegram_id, 'user_id'),
                                                                                            zipcode=return_param(telegram_id, 'zipcode'),
                                                                                            store_name=return_param(telegram_id, 'store_name'),
                                                                                            store_phone=return_param(telegram_id, 'store_phone'),
                                                                                            order_number=return_param(telegram_id, 'order_number'),
                                                                                            pickup_person=return_param(telegram_id, 'pickup_person'),
                                                                                            pickup_location=return_param(telegram_id, 'pickup_location'),
                                                                                            more_info=return_param(telegram_id, 'more_info'),
                                                                                            product_item=return_param(telegram_id, 'product_item'),
                                                                                            price=return_param(telegram_id, 'price')))
        return json.loads(request.text)
    except Exception as err:
        print(err)


def get_category(telegram_id):
    try:
        request = requests.get('https://strongbox.cc/?a=fnc.api.list.getcategory&tuser={user_id}&zip={zipcode}'.format(
            user_id=return_param(telegram_id, 'user_id'),
            zipcode=return_param(telegram_id, 'zipcode')))
        return json.loads(request.text)
    except Exception as err:
        print(err)


def get_items(telegram_id):
    try:
        request = requests.get('https://strongbox.cc/?a=fnc.api.list.getitems&tuser={user_id}&zip={zipcode}&list_id={list_id}'.format(
            user_id=return_param(telegram_id, 'user_id'),
            zipcode=return_param(telegram_id, 'zipcode'),
            list_id=return_param(telegram_id, 'list_id')))
        return json.loads(request.text)
    except Exception as err:
        print(err)


def get_status(telegram_id):
    try:
        request = requests.get('https://strongbox.cc/?a=fnc.api.package.getstatus&tuser={user_id}'.format(
            user_id=return_param(telegram_id, 'user_id')))
        return json.loads(request.text)
    except Exception as err:
        print(err)


def payment(telegram_id):
    try:
        request = requests.get('https://strongbox.cc/?a=fnc.api.package.payment&tuser={user_id}&pack_id={pack_id}&payout={payout}'.format(
            user_id=return_param(telegram_id, 'user_id'),
            pack_id=return_param(telegram_id, 'pack_id'),
            payout=return_param(telegram_id, 'payout')))
        return json.loads(request.text)
    except Exception as err:
        print(err)


def sort_by_dist(response):
    return response['distance'].replace("'", '')
