import sys
import csv
import datetime
import requests
sys.path.insert(0, '../')

from settings import WEBAPP_URL, PRODUCTS_LOCAL_PATH
UPLOAD_URL = WEBAPP_URL + '/upload_bulk'

with open(PRODUCTS_LOCAL_PATH) as f:
    csv_reader = csv.DictReader(f, fieldnames=(
        'sku', 'name', 'regularPrice', 'salePrice', 'type', 'url', 'image', 'inStoreAvailability'))
    total_count = 0
    c = 0
    skip_lines = 0
    item_lst = []
    for line in csv_reader:
        total_count += 1
        if total_count < skip_lines:
            continue
        c += 1
        item_lst.append({
            'sku': line['sku'],
            'name': line['name'],
            'price': line['regularPrice'],
            'type': line['type'],
            'url': line['url']

        })
        if c == 200:
            r = requests.post(UPLOAD_URL, json=item_lst)
            if r.status_code != 200:
                print r.text
                break
            c = 0
            item_lst = []

        if not total_count % 10000:
            print total_count, datetime.datetime.now()
