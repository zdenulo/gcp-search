"""Extracts product from xml files to one csv file
Set data_folder according your case
"""

import os
import csv

import xmltodict

data_folder = '/home/zdenulo/Downloads/product_data/products/'

output_filename = 'best_buy_products.csv'

xml_files = os.listdir(data_folder)


def get_products_from_file(filename, csv_writer):
    print (filename)
    with open(filename) as f:
        c = f.read()
    d = xmltodict.parse(c)

    products = d['products']['product']

    for item in products:
        sku = item['sku']
        name = item['name']
        regular_price = item.get('regularPrice', '')
        sale_price = item.get('salePrice', '')
        typex = item.get('type', '')
        upc = item.get('upc', '')
        url = item.get('url', '')
        image = item.get('image', '')
        inStoreAvailability = item.get('inStoreAvailability', 'false')
        if inStoreAvailability == 'false':
            inStoreAvailability = False
        else:
            inStoreAvailability = True

        data = {
            'sku': sku,
            'name': name,
            'regularPrice': regular_price,
            'salePrice': sale_price,
            'type': typex,
            # 'upc': upc,
            'url': url,
            'image': image,
            'inStoreAvailability': inStoreAvailability

        }
        csv_writer.writerow(data)


if __name__ == '__main__':
    with open(output_filename, 'w') as fout:
        csv_writer = csv.DictWriter(fout, fieldnames=(
            'sku', 'name', 'regularPrice', 'salePrice', 'type', 'url', 'image', 'inStoreAvailability'))
        xml_files = sorted(os.listdir(data_folder))
        for filename in xml_files:
            full_path = os.path.join(data_folder, filename)
            get_products_from_file(full_path, csv_writer)
