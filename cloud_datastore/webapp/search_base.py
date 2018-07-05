class SearchEngine:
    """Base class to implement search interface for different storages"""

    def __init__(self, client=None):
        self.client = client

    def search(self, query):
        """Executes search"""
        raise NotImplementedError

    def insert(self, item):
        """Inserts one item"""
        raise NotImplementedError

    def insert_bulk(self, items):
        """Insert list of times"""
        raise NotImplementedError

    def delete_all(self):
        """Deletes all data"""
        raise NotImplementedError
