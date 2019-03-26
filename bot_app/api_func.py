import requests
import json


class Api:
    def __init__(self, user_id='', zipcode='', store_name='', store_phone='', order_number='', pickup_person='',
                 pickup_location='', more_info='', product_category='', product_item='', price='', pack_id='',
                 payout='', list_id=''):
        self.user_id = user_id
        self.zipcode = zipcode
        self.store_name = store_name
        self.store_phone = store_phone
        self.order_number = order_number
        self.pickup_person = pickup_person
        self.pickup_location = pickup_location
        self.more_info = more_info
        self.product_category = product_category
        self.product_item = product_item
        self.price = price
        self.pack_id = pack_id
        self.payout = payout
        self.list_id = list_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_zipcode(self, zipcode):
        self.zipcode = zipcode

    def set_store_name(self, store_name):
        self.store_name = store_name

    def set_store_phone(self, store_phone):
        self.store_phone = store_phone

    def set_order_number(self, order_number):
        self.order_number = order_number

    def set_pickup_person(self, pickup_person):
        self.pickup_person = pickup_person

    def set_pickup_location(self, pickup_location):
        self.pickup_location = pickup_location

    def set_more_info(self, more_info):
        self.more_info = more_info

    def set_product_category(self, product_category):
        self.product_category = product_category

    def set_product_item(self, product_item):
        self.product_item = product_item

    def set_price(self, price):
        self.price = price

    def set_pack_id(self, pack_id):
        self.pack_id = pack_id

    def set_payout(self, payout):
        self.payout = payout

    def set_list_id(self, list_id):
        self.list_id = list_id

    def return_zipcode(self):
        return self.zipcode

    def __repr__(self):
        return ('{} {}\n'*14).format('user_id =', self.user_id, 'zipcode =', self.zipcode, 'store_name =', self.store_name,
                                     'store_phone =', self.store_phone, 'order_number =', self.order_number,
                                     'pickup_person =', self.pickup_person, 'pickup_location =', self.pickup_location,
                                     'more_info =', self.more_info, 'product_category =', self.product_category,
                                     'product_item =', self.product_item, 'price =', self.price, 'pack_id =', self.pack_id,
                                     'payout =', self.payout, 'list_id =', self.list_id)

    def get_distance(self):
        try:
            request = requests.get('https://strongbox.cc/?a=fnc.api.zip.getdistance&zip={zipcode}&tuser={user_id}'.format(
                zipcode=self.zipcode,
                user_id=self.user_id))
            return json.loads(request.text)
        except Exception as err:
            print(err)

    def get_all(self):
        try:
            request = requests.get('https://strongbox.cc/?a=fnc.api.list.getall&tuser={user_id}&zip={zipcode}'.format(
                user_id=self.user_id,
                zipcode=self.zipcode))
            return json.loads(request.text)
        except Exception as err:
            print(err)

    def add_data(self):
        try:
            request = requests.get('https://strongbox.cc/?a=fnc.api.package.add&tuser={user_id}&zip={zipcode}&store_name={store_name}'
                                   '&store_phone={store_phone}&order_number={order_number}&pickup_person={pickup_person}'
                                   '&pickup_location={pickup_location}&more_information={more_info}&product_category={product_category}'
                                   '&product_item={product_item}&product_price={price}'.format(user_id=self.user_id,
                                                                                               zipcode=self.zipcode,
                                                                                               store_name=self.store_name,
                                                                                               store_phone=self.store_phone,
                                                                                               order_number=self.order_number,
                                                                                               pickup_person=self.pickup_person,
                                                                                               pickup_location=self.pickup_location,
                                                                                               more_info=self.more_info,
                                                                                               product_category=self.product_category,
                                                                                               product_item=self.product_item,
                                                                                               price=self.price))
            return json.loads(request.text)
        except Exception as err:
            print(err)

    def get_category(self):
        try:
            request = requests.get('https://strongbox.cc/?a=fnc.api.list.getcategory&tuser={user_id}&zip={zipcode}'.format(
                user_id=self.user_id,
                zipcode=self.zipcode))
            return json.loads(request.text)
        except Exception as err:
            print(err)

    def get_items(self):
        try:
            request = requests.get('https://strongbox.cc/?a=fnc.api.list.getitems&tuser={user_id}&zip={zipcode}&list_id={list_id}'.format(
                user_id=self.user_id,
                zipcode=self.zipcode,
                list_id=self.list_id))
            return json.loads(request.text)
        except Exception as err:
            print(err)

    def get_status(self):
        try:
            request = requests.get('https://strongbox.cc/?a=fnc.api.package.getstatus&tuser={user_id}'.format(
                user_id=self.user_id))
            return json.loads(request.text)
        except Exception as err:
            print(err)

    def payment(self):
        try:
            request = requests.get('https://strongbox.cc/?a=fnc.api.package.payment&tuser={user_id}&pack_id={pack_id}&payout={payout}'.format(
                user_id=self.user_id,
                pack_id=self.pack_id,
                payout=self.payout))
            return json.loads(request.text)
        except Exception as err:
            print(err)


def sort_by_dist(response):
    return response['distance'].replace("'", '')
