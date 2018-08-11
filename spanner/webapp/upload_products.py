"""
Script to load data from csv file with products data into database
"""

import csv
import sys
import datetime
from spanner_search import SpannerSearch
sys.path.insert(0, '../../')


from settings import PRODUCTS_LOCAL_PATH


if __name__ == '__main__':

    db_client = SpannerSearch()
    db_client.init_schema()
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
                'sale_price': line['salePrice'],
                'type': line['type'],
                'url': line['url'],
                'available': line['inStoreAvailability'],
            })
            if c == 2000:
                db_client.insert_bulk(item_lst)
                c = 0
                item_lst = []

            if not total_count % 10000:
                print(total_count, datetime.datetime.now())
