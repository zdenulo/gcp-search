from search_base import SearchEngine

from google.appengine.api import search


class SearchAPI(SearchEngine):
    """GAE Search API implementation, can be used only withing GAE"""

    def __init__(self, client=None):
        self.client = search.Index('products')  # setting Index

    def search(self, query):
        """Making search with SearchAPI and returning result"""
        try:
            search_results = self.client.search(query)
            results = search_results.results
            output = []
            for item in results:
                out = {
                    'value': item.field('name').value,
                    'label': item.field('name').value,
                    'sku': item.field('sku').value
                }
                output.append(out)
        except Exception:
            output = []
        return output

    def insert(self, item):
        """Inserts document in the Search Index"""
        doc = search.Document(
            fields=[
                search.TextField(name='name', value=item['name']),
                search.TextField(name='sku', value=item['sku']),
            ]
        )
        self.client.put(doc)

    def insert_bulk(self, items):
        """Inserts list of items (dictionaries) into Search Index"""
        docs = []
        for item in items:
            doc = search.Document(
                fields=[
                    search.TextField(name='name', value=item['name']),
                    search.TextField(name='sku', value=item['sku']),
                ]
            )
            docs.append(doc)
        self.client.put(docs)

    def delete_all(self):
        """Deletes all documents in Search Index"""

        while True:
            document_ids = [
                document.doc_id
                for document
                in self.client.get_range(ids_only=True)]

            # If no IDs were returned, we've deleted everything.
            if not document_ids:
                break

            # Delete the documents for the given IDs
            self.client.delete(document_ids)
