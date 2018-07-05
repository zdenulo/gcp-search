import re

from google.appengine.ext import ndb

regex_replace = re.compile('[\W_]+')


class Product(ndb.Model):
    """Datastore model representing product"""
    partial_strings = ndb.StringProperty(repeated=True)
    product_name = ndb.StringProperty()
    price = ndb.FloatProperty()
    url = ndb.StringProperty()
    type = ndb.StringProperty()

    def _pre_put_hook(self):
        """Before save, parse product name into strings"""
        if self.product_name:
            product_name_lst = regex_replace.sub(' ', self.product_name.lower()).split(' ')
            product_name_lst = [x for x in product_name_lst if x and len(x) > 2]
            self.partial_strings = product_name_lst

    @classmethod
    def search(cls, text_query):
        """Execute search query"""
        words = text_query.lower().split(' ')
        words = [w for w in words if w]
        query = cls.query()
        for word in words:
            query = query.filter(cls.partial_strings == word)
        return query.fetch(20)

    @classmethod
    def create(cls, item):
        """Create object (doesn't save)"""
        key = ndb.Key(cls, int(item['sku']))
        obj = cls(key=key, price=float(item['price']), product_name=item['name'], url=item['url'], type=item['type'])
        return obj
