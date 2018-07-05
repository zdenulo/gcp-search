from search_base import SearchEngine
from models import Product

from google.appengine.ext import ndb


class DatastoreSearchAPI(SearchEngine):
    def insert_bulk(self, items):
        to_save = []
        for item in items:
            product = Product.create(item)
            to_save.append(product)
        ndb.put_multi(to_save)

    def insert(self, item):
        product = Product.create(item)
        product.put()

    def search(self, query):
        results = Product.search(query)
        output = []
        for item in results:
            out = {
                'value': item.product_name,
                'label': item.product_name,
                'sku': item.key.id()
            }
            output.append(out)
        return output

    def delete_all(self):
        run = True
        while run:
            res = Product.query().fetch(limit=100, keys_only=True)
            if res:
                ndb.delete_multi(res)
            else:
                run = False
