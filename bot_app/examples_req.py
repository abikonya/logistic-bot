import json


get_distance = {"address": [{"zip": "65721", "distance": "'238'", "name": "AMBER GREENSLATE", "id": "5085"},
                            {"zip": "12345", "distance": "'435'", "name": "AMBER GREENSLATE", "id": "5085"},
                            {"zip": "45678", "distance": "'245'", "name": "AMBER GREENSLATE", "id": "5085"},
                            {"zip": "23567", "distance": "'234'", "name": "AMBER GREENSLATE", "id": "5085"}]}

spisok = json.dumps(get_distance)
spisok_dict = json.loads(spisok)
spisok_list = spisok_dict['address']


# class ZipList:
#     def __init__(self, addresses):
#         self.zip = each['zip']
#         self.distance = int(each['distance'].replace("'", ''))
#         self.name = each['name']
#
#     def __repr__(self):
#         result = dict()
#         result['zip'] = self.zip
#         result['distance'] = self.distance
#         result['name'] = self.name
#         return result


def sort_by_dist(spisok_list):
    return spisok_list['distance'].replace("'", '')


a = sorted(spisok_list, key=sort_by_dist)
print(a)
