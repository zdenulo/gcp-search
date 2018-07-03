"""
Get all words in product names and sort by most occurrences.
output file is used in load testing
"""

import csv

# absolute path to best_buy_products.csv
INPUT_FILE = ''

words_dict = dict()
with open(INPUT_FILE) as f:
    csv_reader = csv.DictReader(f, fieldnames=(
        'sku', 'name', 'regularPrice', 'salePrice', 'type', 'url', 'image', 'inStoreAvailability'))
    for line in csv_reader:
        name = line['name']
        words = name.split(' ')
        words = [w.strip() for w in words]
        for word in words:
            count = words_dict.get(word, 0)
            count += 1
            words_dict[word] = count


ordered_words = sorted(words_dict.iteritems(), key=lambda x: x[1], reverse=True)

with open('words.csv', 'w') as f:
    csv_writer = csv.DictWriter(f, fieldnames=('word', 'count'))
    csv_writer.writeheader()
    for line in ordered_words:
        csv_writer.writerow({
            'word': line[0],
            'count': line[1]
        })
