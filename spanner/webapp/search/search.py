

class SearchEngine:
    """Base class to implement search interface for different storages"""

    def __init__(self, client=None):
        self.client = client

    def search(self, query):
        """Executes search"""
        raise NotImplementedError

    def insert(self, text):
        """Inserts text"""
        raise NotImplementedError

