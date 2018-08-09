"""
Database stuff
"""

import os
import sqlalchemy
from sqlalchemy import create_engine, Column, String, Float, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import search
from sqlalchemy_searchable import sync_trigger

from db_settings import USERNAME, PASSWORD, DB_NAME


SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']

if not SQLALCHEMY_DATABASE_URI:
    SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://{USER_NAME}:{PASSWORD}@127.0.0.1:5431/{DATABASE_NAME}'.format(
        USER_NAME=USERNAME, PASSWORD=PASSWORD, DATABASE_NAME=DB_NAME
    )

# these are some necessary lines
Base = declarative_base()
make_searchable(Base.metadata)
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
sqlalchemy.orm.configure_mappers()

Session = sessionmaker(bind=engine)
session = Session()


class Product(Base):
    """Table for products"""
    __tablename__ = 'products'

    sku = Column(BigInteger, primary_key=True)
    product_name = Column(String)
    price = Column(Float)
    sale_price = Column(Float)
    type = Column(String)
    url = Column(String)
    image = Column(String)
    available = Column(String)
    search_vector = Column(TSVectorType('product_name', ))  # this field is for full text search

    def __repr__(self):
        return self.product_name


class PostgreSQLSearch():
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
        objects = []
        for product in product_data:
            if product.get('name', ''):
                product_db = Product(sku=product['sku'], product_name=product['name'], price=product['price'],
                                     url=product['url'], type=product['type'], available=product['available'],
                                     sale_price=product['sale_price'], image=product['image']
                                     )
                objects.append(product_db)
        session.bulk_save_objects(objects)
        session.commit()

    def search(self, search_query):
        """making query to database"""
        query = session.query(Product)
        query = search(query, search_query, sort=True)
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


if __name__ == '__main__':
    db_client = PostgreSQLSearch()
    db_client.init_schema()
