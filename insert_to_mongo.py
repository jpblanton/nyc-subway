import os
import json
from pathlib import Path

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(override=True)

dbstr = os.getenv('MONGO_STR')
pwd = '1234' # will be stored elsewhere if I switch to a real pwd

client = MongoClient(dbstr.format(password=pwd))
db = client['nyc-subway']

target_paths = [fp for fp in Path('data').glob('*') if fp.is_dir()]

for dir_ in target_paths:
    colname = dir_.name
    this_col = db[colname]
    all_json = []
    for fp in dir_.glob('*.json'):
        time = int(fp.stem)
        temp = json.load(fp.open('r'))
        for e in temp['entity']:
            e['ts'] = time
        this_col.insert_many(temp['entity'])
