#!/usr/bin/python3

import json
import os
import requests
from datetime import datetime

from protobuf_to_dict import protobuf_to_dict
from google.transit import gtfs_realtime_pb2 as gtfs

#api_key = os.getenv('MTAACCESSKEY')
with open('/home/james/Projects/nyc-subway/access_key.txt', 'r') as f:
    api_key = f.read().strip()

headers = {'x-api-key': api_key}

with open('/home/james/Projects/nyc-subway/feeds.json', 'r') as f:
    feeds_dict = json.load(f)

feed_obj = gtfs.FeedMessage()
# want to have uniform timestamps
time = str(datetime.now().timestamp()).split('.')[0]
for name in feeds_dict:
    url = feeds_dict[name]
    resp = requests.get(url, headers=headers)
    feed_obj.ParseFromString(resp.content)
    temp = protobuf_to_dict(feed_obj)
    fn = f'/home/james/Projects/nyc-subway/data/{name}/{time}.json'
    with open(fn, 'w') as f:
        json.dump(temp, f)
    globals()[name] = temp

