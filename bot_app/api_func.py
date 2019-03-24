import requests


class Api:
    def __init__(self, user_id=None, zipcode=None, store_name=None, store_phone=None, order_number=None, pickup_person=None,
                 pickup_location=None, more_info=None, product_category=None, product_item=None, price=None, pack_id=None,
                 payout=None, list_id=None):
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

    def __repr__(self):
        return ('{} {}\n'*14).format('user_id =', self.user_id, 'zipcode =', self.zipcode, 'store_name =', self.store_name,
                                     'store_phone =', self.store_phone, 'order_number =', self.order_number,
                                     'pickup_person =', self.pickup_person, 'pickup_location =', self.pickup_location,
                                     'more_info =', self.more_info, 'product_category =', self.product_category,
                                     'product_item =', self.product_item, 'price =', self.price, 'pack_id =', self.pack_id,
                                     'payout =', self.payout, 'list_id =', self.list_id)

    def get_distance(self):
        request = requests.get('https://strongbox.cc/?a=fnc.api.zip.getdistance&zip={zipcode}&tuser={user_id}'.format(
            zipcode=self.zipcode,
            user_id=self.user_id))
        return request

    def get_all(self):
        request = requests.get('https://strongbox.cc/?a=fnc.api.list.getall&tuser={user_id}&zip={zipcode}'.format(
            user_id=self.user_id,
            zipcode=self.zipcode))
        return request

    def add_data(self):
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
        return request

    def get_category(self):
        request = requests.get('https://strongbox.cc/?a=fnc.api.list.getcategory&tuser={user_id}&zip={zipcode}'.format(
            user_id=self.user_id,
            zipcode=self.zipcode))
        return request

    def get_items(self):
        request = requests.get('https://strongbox.cc/?a=fnc.api.list.getitems&tuser={user_id}&zip={zipcode}&list_id={list_id}'.format(
            user_id=self.user_id,
            zipcode=self.zipcode,
            list_id=self.list_id))
        return request

    def get_status(self):
        request = requests.get('https://strongbox.cc/?a=fnc.api.package.getstatus&tuser={user_id}'.format(
            user_id=self.user_id))
        return request

    def payment(self):
        request = requests.get('https://strongbox.cc/?a=fnc.api.package.payment&tuser={user_id}&pack_id={pack_id}&payout={payout}'.format(
            user_id=self.user_id,
            pack_id=self.pack_id,
            payout=self.payout))
        return request


def sort_by_dist(response):
    return response['distance'].replace("'", '')
