from search.search import SearchEngine

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy import select, cast
from sqlalchemy.orm.mapper import configure_mappers
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import search
from sqlalchemy_searchable import sync_trigger


# set this accordingly
USERNAME = 'postgres'
PASSWORD = 'qwert'
HOST = '35.198.119.207'
DB_NAME = 'products'
###

CONNECTION = 'postgresql+psycopg2://{username}:{password}@{host}:5432/{dbname}'.format(username=USERNAME,
                                                                                       password=PASSWORD,
                                                                                       host=HOST,
                                                                                       dbname=DB_NAME)

# these are some necessary lines
Base = declarative_base()
make_searchable()
engine = create_engine(CONNECTION, echo=True)
sqlalchemy.orm.configure_mappers()

Session = sessionmaker(bind=engine)
session = Session()


class Product(Base):
    """Table for products"""
    __tablename__ = 'products'

    sku = Column(Integer, primary_key=True)
    product_name = Column(String)
    price = Column(Float)
    upc = Column(String)
    description = Column(String)
    url = Column(String)
    search_vector = Column(TSVectorType('product_name', ))  # this field is for full text search

    def __repr__(self):
        return self.product_name


class PostgreSQLSearch(SearchEngine):
    def init_schema(self):
        """creates table"""
        # configure_mappers()
        session.commit()  # with out this line, Flask hangs for some reason
        Base.metadata.create_all(engine)
        sync_trigger(engine, 'products', 'search_vector', ['product_name'])

    def delete_all(self):
        """deletes table"""
        session.commit()  # with out this line, Flask hangs for some reason
        Product.__table__.drop(engine)

    def insert_bulk(self, product_data):
        """creates multiple row (objects) and commits into database"""
        total_count = 0
        for product in product_data:
            if product.get('name', ''):
                product_db = Product(sku=product['sku'], product_name=product['name'], price=product['price'],
                                     upc=product['upc'], description=product['description'], url=product['url']
                                     )

                session.add(product_db)
                total_count += 1
                if not total_count % 1000:
                    print(total_count)
                    session.flush()
        session.commit()

    def search(self, search_query):
        """making query to database"""
        query = session.query(Product)
        query = search(query, search_query)
        results = query.limit(20).all()
        output = []
        for item in results:
            out = {
                'value': item.product_name,
                'label': item.product_name,
                'sku': item.sku
            }
            output.append(out)
        return output
