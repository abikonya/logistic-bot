attrib = {'user_id': '',
          'zipcode': '',
          'store_name': '',
          'store_phone': '',
          'order_number': '',
          'pickup_person': '',
          'pickup_location': '',
          'more_info': '',
          'product_category': '',
          'product_item': '',
          'price': '',
          'pack_id': '',
          'payout': '',
          'list_id': '',
          }

get_distance = 'https://strongbox.cc/?a=fnc.api.zip.getdistance&zip={zipcode}&tuser={user_id}'.format(**attrib)


def sort_by_dist(response):
    return response['distance'].replace("'", '')


get_all = 'https://strongbox.cc/?a=fnc.api.list.getall&tuser={user_id}&zip={zipcode}'.format(**attrib)

add_data = 'https://strongbox.cc/?a=fnc.api.package.add&tuser={user_id}&zip={zipcode}&store_name={store_name}' \
           '&store_phone={store_phone}&order_number={order_number}&pickup_person={pickup_person}' \
           '&pickup_location={pickup_location}&more_information={more_info}&product_category={product_category}' \
           '&product_item={product_item}&product_price={price}'.format(**attrib)


get_category = 'https://strongbox.cc/?a=fnc.api.list.getcategory&tuser={user_id}&zip={zipcode}'.format(**attrib)

get_items = 'https://strongbox.cc/?a=fnc.api.list.getitems&tuser={user_id}&zip={zipcode}&list_id={list_id}'.format(**attrib)

get_status = 'https://strongbox.cc/?a=fnc.api.package.getstatus&tuser={user_id}'.format(**attrib)

payment = 'https://strongbox.cc/?a=fnc.api.package.payment&tuser={user_id}&pack_id={pack_id}&payout={payout}'.format(**attrib)
