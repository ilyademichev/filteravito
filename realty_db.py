import urllib

import pyodbc
from sqlalchemy import create_engine, MetaData,Table
#Create and engine and get the metadata
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session

Base = declarative_base()
engine = create_engine("access+pyodbc://@your_dsn")
metadata = MetaData(bind=engine)

connection_string = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    # r'UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;'
    # r'PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL=MS Access;'
    # r'DriverId=25;DefaultDir=C:\REALTYDB;'
    r'DBQ=C:\REALTYDB\realty.accdb;'
    r'ExtendedAnsiSQL=1;')
# engine = create_engine(connection_string)
class RealtyItem(Base):
    __tablename__ = Table('Запись', metadata, autoload=True)

class Company(Base):
    __tablename__ = Table('Организации', metadata, autoload=True)

class Rooms(Base):
    __tablename__ = Table('Число комнат', metadata, autoload=True)

class AdvertismentSource(Base):
    __tablename__ = Table('Источники', metadata, autoload=True)



connection_url = f"access+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}"
engine = create_engine(connection_url)
session = create_session(bind=engine)
q = session.query(RealtyItem)
res = q.all()
session.close()
engine.dispose()


