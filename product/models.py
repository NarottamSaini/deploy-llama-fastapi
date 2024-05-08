'''
Create SQLAlchemy models from the Base class
Tip::
SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database.
But Pydantic also uses the term "model" to refer to something different, the data validation, conversion, and documentation classes and instances.
Import Base from database (the file database.py from above).
Create classes that inherit from it. These classes are the SQLAlchemy models.
'''
from sqlalchemy import Boolean, Column,  Integer, String  ##ForeignKey,
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = 'products'  ## db table name
    index = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    # seller_id = Column(Integer, ForeignKey('sellers.id'))
    # seller = relationship("Seller", back_populates='products')

# class Seller(Base):
#     __tablename__ = "sellers" ## db table name
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String)
#     email = Column(String)
#     password = Column(String)
#     # products = relationship('Product', back_populates='seller')

class User(Base):
    __tablename__ = "users" ## db table name
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    # products = relationship('Product', back_populates='seller')

class Temp_table(Base):
    __tablename__ = 'temp_table'
    index = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)

    