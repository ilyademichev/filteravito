from typing import re

import inflect as inflect
import pyodbc
# from sqlalchemy import registry
from sqlalchemy.orm import sessionmaker
# from snowflake.sqlalchemy import URL
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from sqlalchemy import Column, ForeignKey, Integer, String, MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import urllib

# import sqlalchemy.dialects.


# fixed_dialect_mod.dialect = FixedAccessDialect
# sqlalchemy.dialects.access.fix = fixed_dialect_mod
# fixup_access()
# ENGINE = sqlalchemy.create_engine('access+fix://admin@/%s' % (db_location))

ABase = automap_base()
Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Address(Base):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)


# class Zap(Base):
#     __tablename__ = 'Запись'
#     phone = Column(String(255))
def camelize_classname(base, tablename, table):
    "Produce a 'camelized' class name, e.g. "
    "'words_and_underscores' -> 'WordsAndUnderscores'"

    return str(tablename[0].upper() + \
               re.sub(r'_([a-z])', lambda m: m.group(1).upper(), tablename[1:]))


_pluralizer = inflect.engine()


def pluralize_collection(base, local_cls, referred_cls, constraint):
    "Produce an 'uncamelized', 'pluralized' class name, e.g. "
    "'SomeTerm' -> 'some_terms'"

    referred_name = referred_cls.__name__
    uncamelized = re.sub(r'[A-Z]',
                         lambda m: "_%s" % m.group(0).lower(),
                         referred_name)[1:]
    pluralized = _pluralizer.plural(uncamelized)
    print((pluralized))
    return pluralized


connection_string = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    # r'UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;'
    # r'PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL=MS Access;'
    # r'DriverId=25;DefaultDir=C:\REALTYDB;'
    r'DBQ=C:\REALTYDB\realty.accdb;'
    r'ExtendedAnsiSQL=1;')
# engine = create_engine(connection_string)
connection_url = f"access+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}"
engine = create_engine(connection_url)
# ABase.prepare(engine, reflect=True,
#               classname_for_table=camelize_classname,
#               name_for_collection_relationship=pluralize_collection
#               )
# # zap = ABase.classes
# for c in ABase.classes:
#     print(c)
# session = Session(engine)
# session.add(zap("test"))
# session.commit()
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
# Base.metadata.create_all(engine)
# conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\REALTYDB\realty.accdb;')
# cursor = conn.cursor()
# cursor.execute("SELECT Запись.Торг,Запись.[Дата Подачи] from Запись where cint(Запись.Торг)=-1" )
# cursor.execute("SELECT Запись.[Телефон 1*], Запись.[Цена*1000] from Запись " )
# for row in cursor.fetchall():

#       print(*row)
metadata = MetaData()
ABase = automap_base(metadata=metadata)
ABase.prepare(classname_for_table=camelize_classname,
             name_for_collection_relationship=pluralize_collection
      )
# # reflect db schema to MetaData
metadata.reflect(bind=engine)
ex_table = metadata.tables['Запись']
col_num = 1
columns = [(m.key, m.type) for m in ex_table.columns]
# types = [col.type for col in ex_table.columns]
print(*columns, sep='\n')
# while col_num < len(types):
#     try:
#         c = columns[col_num]
#         print(c)
#     except:
#         pass
#     finally:
#         col_num += 1
engine.dispose()
