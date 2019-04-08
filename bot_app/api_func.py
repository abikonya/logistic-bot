import requests
import json
from vedis import Vedis


class Api:
    def __init__(self):
        with Vedis('tech_info.vdb') as db:
            self.db = db

    def set_user_id(self, telegram_id, user_id):
        account = self.db.Hash(telegram_id)
        account['user_id'] = user_id

    def set_zipcode(self, telegram_id, zipcode):
        account = self.db.Hash(telegram_id)
        account['zipcode'] = zipcode

    def set_store_name(self, telegram_id, store_name):
        account = self.db.Hash(telegram_id)
        account['store_name'] = store_name

    def set_store_phone(self, telegram_id, store_phone):
        account = self.db.Hash(telegram_id)
        account['store_phone'] = store_phone

    def set_order_number(self, telegram_id, order_number):
        account = self.db.Hash(telegram_id)
        account['order_number'] = order_number

    def set_pickup_person(self, telegram_id, pickup_person):
        account = self.db.Hash(telegram_id)
        account['pickup_person'] = pickup_person

    def set_pickup_location(self, telegram_id, pickup_location):
        account = self.db.Hash(telegram_id)
        account['pickup_location'] = pickup_location

    def set_more_info(self, telegram_id, more_info):
        account = self.db.Hash(telegram_id)
        account['more_info'] = more_info

    def set_product_category(self, telegram_id, product_category):
        account = self.db.Hash(telegram_id)
        account['product_category'] = product_category

    def set_product_item(self, telegram_id, product_item):
        account = self.db.Hash(telegram_id)
        account['product_item'] = product_item

    def set_price(self, telegram_id, price):
        account = self.db.Hash(telegram_id)
        account['price'] = price

    def set_pack_id(self, telegram_id, pack_id):
        account = self.db.Hash(telegram_id)
        account['pack_id'] = pack_id

    def set_payout(self, telegram_id, payout):
        account = self.db.Hash(telegram_id)
        account['payout'] = payout

    def set_list_id(self, telegram_id, list_id):
        account = self.db.Hash(telegram_id)
        account['list_id'] = list_id

    def return_param(self, telegram_id, param):
        account = self.db.Hash(telegram_id)
        return account[param].decode('UTF-8')

    def get_distance(self, telegram_id):
        try:
            request = requests.get('https://strongbox.cc/?a=fnc.api.zip.getdistance&zip={zipcode}&tuser={user_id}'.format(
                zipcode=self.return_param(telegram_id, 'zipcode'),
                user_id=self.return_param(telegram_id, 'user_id')))
            return json.loads(request.text)
        except Exception as err:
            print(err)

    def get_all(self, telegram_id, offset):
        try:
            request = requests.get('https://strongbox.cc/?a=fnc.api.list.getall&tuser={user_id}&zip={zipcode}&count=10&offset={offset}'.format(
                user_id=self.return_param(telegram_id, 'user_id'),
                zipcode=self.return_param(telegram_id, 'zipcode'),
                offset=offset))
            return json.loads(request.text)
        except Exception as err:
            print(err)

    def add_data(self, telegram_id):
        try:
            request = requests.get('https://strongbox.cc/?a=fnc.api.package.add&tuser={user_id}&zip={zipcode}&store_name={store_name}'
                                   '&store_phone={store_phone}&order_number={order_number}&pickup_person={pickup_person}'
                                   '&pickup_location={pickup_location}&more_information={more_info}'
                                   '&product_item={product_item}&product_price={price}'.format(user_id=self.return_param(telegram_id, 'user_id'),
                                                                                               zipcode=self.return_param(telegram_id, 'zipcode'),
                                                                                               store_name=self.return_param(telegram_id, 'store_name'),
                                                                                               store_phone=self.return_param(telegram_id, 'store_phone'),
                                                                                               order_number=self.return_param(telegram_id, 'order_number'),
                                                                                               pickup_person=self.return_param(telegram_id, 'pickup_person'),
                                                                                               pickup_location=self.return_param(telegram_id, 'pickup_location'),
                                                                                               more_info=self.return_param(telegram_id, 'more_info'),
                                                                                               product_item=self.return_param(telegram_id, 'product_item'),
                                                                                               price=self.return_param(telegram_id, 'price')))
            return json.loads(request.text)
        except Exception as err:
            print(err)

    def get_category(self, telegram_id):
        try:
            request = requests.get('https://strongbox.cc/?a=fnc.api.list.getcategory&tuser={user_id}&zip={zipcode}'.format(
                user_id=self.return_param(telegram_id, 'user_id'),
                zipcode=self.return_param(telegram_id, 'zipcode')))
            return json.loads(request.text)
        except Exception as err:
            print(err)

    def get_items(self, telegram_id):
        try:
            request = requests.get('https://strongbox.cc/?a=fnc.api.list.getitems&tuser={user_id}&zip={zipcode}&list_id={list_id}'.format(
                user_id=self.return_param(telegram_id, 'user_id'),
                zipcode=self.return_param(telegram_id, 'zipcode'),
                list_id=self.return_param(telegram_id, 'list_id')))
            return json.loads(request.text)
        except Exception as err:
            print(err)

    def get_status(self, telegram_id):
        try:
            request = requests.get('https://strongbox.cc/?a=fnc.api.package.getstatus&tuser={user_id}'.format(
                user_id=self.return_param(telegram_id, 'user_id')))
            return json.loads(request.text)
        except Exception as err:
            print(err)

    def payment(self, telegram_id):
        try:
            request = requests.get('https://strongbox.cc/?a=fnc.api.package.payment&tuser={user_id}&pack_id={pack_id}&payout={payout}'.format(
                user_id=self.return_param(telegram_id, 'user_id'),
                pack_id=self.return_param(telegram_id, 'pack_id'),
                payout=self.return_param(telegram_id, 'payout')))
            return json.loads(request.text)
        except Exception as err:
            print(err)


def sort_by_dist(response):
    return response['distance'].replace("'", '')
