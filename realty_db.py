# -*- coding: utf-8 -*-
import urllib

import pyodbc
from sqlalchemy.ext.automap import automap_base

from sqlalchemy import create_engine, MetaData, Table, Column, String, ForeignKey, Integer
#Create and engine and get the metadata
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session, relationship,sessionmaker
#from sqlalchemy. access import Integer
from sqlalchemy.dialects import registry
#registry.register("access", "sqlalchemy_access.pyodbc", "AccessDialect_pyodbc")
#registry.register("access.pyodbc", "sqlalchemy_access.pyodbc", "AccessDialect_pyodbc")


Base = declarative_base()

connection_string = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    # r'UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;'
    # r'PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL=MS Access;'
    # r'DriverId=25;DefaultDir=C:\REALTYDB;'
    r'DBQ=C:\REALTYDB\realty.accdb;'
    r'ExtendedAnsiSQL=1')
# engine = create_engine(connection_string)
connection_url = f"access+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}"



# engine = create_engine(connection_string)
class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class RealtyItem(Base):
    __tablename__ = 'zap'
    # __table__ = Table(__tablename__, metadata, autoload=True,autoload_with=engine)
    #__table__ = init_table('Запись')
    # __mapper_args__ = {
    #     'primary_key': ['Объект*']
    # }
    rooms=Column('Объект*', Integer, primary_key=True)
    floor=Column('Этаж*', String(255), primary_key=True)
    phone=Column('Телефон 1*', String(255), primary_key=True)
    agent_name=Column('Организация*', Integer, primary_key=True)
    forsale_forrent=Column('Актуальность*', Integer, primary_key=True)
    s_property=Column('S общ*/объекта', String(255), primary_key=True)
    s_land=Column('S уч, сот', String(255), primary_key=True)
    address=Column('Адрес', String(255), primary_key=True)
    company_id = Column(Integer, ForeignKey('Организации.Код'))


class Company(Base):
     __tablename__ = 'Организации'
     id = Column('Код', Integer, primary_key=True)
     properties = relationship("RealtyItem", backref="parent")
#
# class Rooms(Base):
#     __tablename__ = Table('Число комнат', metadata, autoload=True)

# class AdvertismentSource(Base):
#     __tablename__ = Table('Источники', metadata, autoload=True)


# user_table = Table('Запись', metadata,
#             Column('id', Integer, primary_key=True),
#             Column('name', String),
#         )



engine = create_engine(connection_url)
#session = create_session(bind=engine)
metadata = MetaData(bind=engine)
ABase = automap_base(metadata=metadata)
ABase.prepare()
metadata.reflect(bind=engine)
ex_table = metadata.tables
cl = ABase.classes.items()
print(cl)
q = session.query(RealtyItem).filter_by(floor='1').all()
print([i.st for i in q])
session.close()
engine.dispose()


