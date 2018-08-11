
from search.search import SearchEngine


from google.cloud import spanner

INSTANCE_ID = 'eshopxx'
DATABASE_ID = 'products'
SERVICE_ACCOUNT_JSON = 'service_account.json'


class SpannerSearch(SearchEngine):

    def __init__(self, client=None):
        client = spanner.Client.from_service_account_json('service_account.json')
        self.instance = client.instance(INSTANCE_ID)
        database = self.instance.database(DATABASE_ID)
        self.client = database

    def init_schema(self):
        """Creates database for instance and table for products"""
        database = self.instance.database(DATABASE_ID, ddl_statements=[
            """CREATE TABLE Products (
            Sku INT64 NOT NULL,
            ProductName STRING(1024) NOT NULL,
            ProductNameCase STRING(1024) NOT NULL,
            Price FLOAT64,
            Upc STRING(1024),
            Description STRING(1024),
            Url STRING(1024)            
            ) PRIMARY KEY (Sku)
            """
        ])
        operation = database.create()
        operation.result()

    def insert_bulk(self, input_data):
        """input is list of dictionaries. fields are sensitive to position in list"""
        values = []
        for item in input_data:
            values.append((item['sku'], item['name'], item['name'].upper(), item['price']*1.0, item['description'], item['upc'], item['url']),)

        with self.client.batch() as batch:
            batch.insert(
                table='products',
                columns=('Sku', 'ProductName', 'ProductNameCase', 'Price', 'Description', 'Upc', 'Url'),
                values=values
            )

    def search(self, query):
        """does search on table with LIKE operator. Number of returned results is set with LIMIT"""
        db_query = """SELECT * FROM products WHERE ProductNameCase LIKE '%{}%' LIMIT 20""".format(query.upper())
        output = []
        with self.client.snapshot() as snapshot:
            results = snapshot.execute_sql(db_query)
            for row in results:
                out = {
                    'value': row[1],
                    'label': row[1]
                }
                output.append(out)
        return output

    def delete_all(self):
        """deletes database (and table)"""
        self.client.drop()