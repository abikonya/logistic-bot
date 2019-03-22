import json


get_distance = {"address": [{"zip": "65721", "distance": "'238'", "name": "AMBER GREENSLATE", "id": "5085"},
                            {"zip": "12345", "distance": "'435'", "name": "AMBER GREENSLATE", "id": "5085"},
                            {"zip": "45678", "distance": "'245'", "name": "AMBER GREENSLATE", "id": "5085"},
                            {"zip": "23567", "distance": "'234'", "name": "AMBER GREENSLATE", "id": "5085"}]}

a = json.dumps(get_distance)

b = json.loads(a)

# for each in b['address']:
#     print(int(each['distance'].replace("'", '')))


def sorting(some_json):
    list_for_sort = json.loads(some_json)['address']
    for each in list_for_sort:
        dist_to_num = each['distance'].replace("'", '')
        print(each)

sorting(a)