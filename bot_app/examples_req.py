import json
from bot_app import api_func

get_distance = {"address": [{"zip": "65721", "distance": "'238'", "name": "AMBER GREENSLATE", "id": "5085"},
                            {"zip": "12345", "distance": "'435'", "name": "AMBER GREENSLATE", "id": "5085"},
                            {"zip": "45678", "distance": "'245'", "name": "AMBER GREENSLATE", "id": "5085"},
                            {"zip": "23567", "distance": "'234'", "name": "AMBER GREENSLATE", "id": "5085"}]}

ans = json.dumps(get_distance)
