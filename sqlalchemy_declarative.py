import datetime
import re
import time

import inflect as inflect
import pyodbc
# from sqlalchemy import registry
from sqlalchemy.orm import sessionmaker
# from snowflake.sqlalchemy import URL
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from sqlalchemy import create_engine, exists, MetaData, and_

from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
#Create and engine and get the metadata
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy_utils import URLType
#from sqlalchemy. access import Intege

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
from parser_logger import parser_logger
from realty_appartment_page import RealtyApartmentPage

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



class RealtyItem(Base):
    __tablename__ = 'Запись'
    # __table__ = Table(__tablename__, metadata, autoload=True,autoload_with=engine)
    #__table__ = init_table('Запись')
    # __mapper_args__ = {
    #     'primary_key': ['Объект*']
    # }
    phone=Column('Телефон 1*', String(255), primary_key=True)
    company_id = Column('Организация*',Integer, ForeignKey('Организации.Код'),primary_key=True)
    rooms=Column('Объект*', Integer,ForeignKey('Число комнат.Код'), primary_key=True)
    address=Column('Адрес', String(255))
    street=Column('Ул/пр*', Integer,ForeignKey('Улици.Код'), primary_key=True)
    house_num=Column('№ дома*', String(255), primary_key=True)
    floor=Column('Этаж*', String(255), primary_key=True)
    #agent_name=Column('Организация*', Integer, )
    s_property=Column('S общ*/объекта', String(255), primary_key=True)
    #s_land=Column('S уч, сот', String(255), primary_key=True)
    forsale_forrent=Column('Актуальность*', Integer,ForeignKey('Продано, на задатке, не отвечает.Код'), primary_key=True)
    description=Column('Примечание 3', LONGTEXT)
    contact_name=Column('Имя 1', String(255))
    url=Column('Ссылка', URLType)
    price=Column('Цена min*1000', String(255))
    # source=Column('Источник', Integer,ForeignKey('Источники.Код'))
    timestamp=Column('Дата Подачи', DateTime)
    call_timestamp=Column('Дата Прозвона/Преостановлено до/Позвонить', DateTime)

class Company(Base):
    __tablename__ = "Организации"
    id = Column('Код', Integer, primary_key=True)
    company_name = Column('Организация', String(255))
     #realty_id = Column(Integer, ForeignKey('users.id'))
    properties = relationship("RealtyItem", backref="Организации",\
                     cascade="all, delete, delete-orphan")

class Rooms(Base):
    __tablename__ = "Число комнат"
    id = Column('Код', Integer, primary_key=True)
    description = Column('Объект', Integer, primary_key=True)
    properties = relationship("RealtyItem", backref="Число комнат", \
                          cascade="all, delete, delete-orphan")

class RealtyStatus(Base):
    __tablename__ = "Продано, на задатке, не отвечает"
    id = Column('Код', Integer, primary_key=True)
    status = Column('Продано', String(255))
    properties = relationship("RealtyItem", backref="Продано, на задатке, не отвечает", \
                              cascade="all, delete, delete-orphan")

class Streets(Base):
    __tablename__ = "Улици"
    id = Column('Код', Integer, primary_key=True)
    street = Column('Улица', String(255))
    properties = relationship("RealtyItem", backref="Улици", \
                              cascade="all, delete, delete-orphan")


# class AdvertismentSource(Base):
#     __tablename__ = "Источники"
#     id = Column('Код', Integer, primary_key=True)
#     source = Column('Источник/Реклама', String(255))
#     properties = relationship("RealtyItem", backref="Источники", \
#                           cascade="all, delete, delete-orphan")




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
engine = create_engine(connection_url,echo=True)
# Base.prepare(engine, reflect=True
#               # classname_for_table=camelize_classname,
#               # name_for_collection_relationship=pluralize_collection
#               )
# ABase.metadata.create_all(engine)
# for c in Base.classes:
#     print(c)
try:
    session = Session(engine)
    # p = session.query(Person).all()
    # a = session.query(Address).all()
    # r = session.query(RealtyItem).all()
    # test item
    c = session.query(Company).filter_by(company_name="-").scalar()
    s = session.query(RealtyStatus).filter_by(status="в Продаже").scalar()
    r = session.query(Rooms).filter_by(description="2").scalar()
    st = session.query(Streets).filter_by(street="-").scalar()
    house_not_identified = '-'
    # so = session.query(AdvertismentSource).filter_by(source="Avito сайт").scalar()
    # session.add(zap("test"))
    realty_item = RealtyItem()
    realty_item.phone = "903810488"
    realty_item.company_id = c.id
    realty_item.rooms = r.id
    realty_item.address = "г. Обнинск, ул. Маркса 63"
    realty_item.floor = "8"
    realty_item.area = "49"
    realty_item.forsale_forrent = s.id
    realty_item.price = "3900000"
    # unable to use nested queries in ms access
    # q = session.query( exists().where(and_(
    #                     RealtyItem.phone == realty_item.phone,
    #                     RealtyItem.company_id == realty_item.company_id,
    #                     RealtyItem.rooms == realty_item.rooms,
    #                     RealtyItem.address == realty_item.address,
    #                     RealtyItem.floor == realty_item.floor,
    #                     RealtyItem.s_property == realty_item.area,
    #                     RealtyItem.forsale_forrent == realty_item.forsale_forrent))).scalar()
    # once multiple items exist MultipleResultsFound raised - compound primary key violation
    q = session.query(RealtyItem).filter_by(
                        phone = realty_item.phone,
                        company_id = realty_item.company_id,
                        rooms = realty_item.rooms,
                        address = realty_item.address,
                        floor = realty_item.floor,
                        s_property = realty_item.area,
                        forsale_forrent = realty_item.forsale_forrent).scalar()
    if not q:
        # compose new item
            t = datetime.date.fromtimestamp(time.time())
            q = RealtyItem(
                phone=realty_item.phone,
                company_id=realty_item.company_id,
                rooms=realty_item.rooms,
                address=realty_item.address,
                street = st.id,
                house_num = house_not_identified,
                floor=realty_item.floor,
                s_property=realty_item.area,
                forsale_forrent=realty_item.forsale_forrent,
                description=realty_item.description,
                contact_name=realty_item.contact_name,
                url="https://m.avito.ru/podolsk/kvartiry/3-k_kvartira_58_m_35_et._2001729439",
                # source=so.id,
                timestamp =  t, # '#2009-04-21 14:25:53#', # datetime.datetime.utcnow(),
                call_timestamp = t #'#2009-04-21 14:25:53#'  # datetime.datetime.utcnow()
                )
            try:
                q.price = str(int(int(realty_item.price) / 1000))
            except ValueError:
                parser_logger.error("Thread  - price conversion failed. Set 0 price . RealtyItem:}")
                q.price = str("")
            #insert new realty item
            session.add(q)
            # rs = engine.connect().execute('INSERT INTO Запись ( Объект*.Value ) \
            # VALUES("Avito робот") WHERE Запись.Объект* In (SELECT Запись.Объект* FROM Источники INNER JOIN Запись \
            # ON Источники.Источник/Реклама = Запись.Объект*) AND Запись.Адрес=г. Обнинск, ул. Шацкого 13 ;')
            #update realty item
    else:
                #set current date
                #set price
                #set source "Avito робот"
                q.timestamp = datetime.date.fromtimestamp(time.time())
                try:
                    q.price = str(int(int(realty_item.price) / 1000))
                except ValueError:
                    parser_logger.error("Thread  - price conversion failed. Set 0 price . RealtyItem:}")
                    q.price = str("")
                # q.source = so.id
                # miltivalued field cannot be altered in Access we run the raw SQL
                # rs = engine.connect().execute('UPDATE Запись SET [Запись].[Объект*] = 2 WHERE [Адрес]=\'г. Обнинск, ул. Шацкого 13\';')

                # rs = engine.connect().execute('INSERT INTO [Запись]([Источник].Value) VALUES ('+str(so.id)+') WHERE (([Запись].[Адрес])=\'г. Обнинск, ул. Маркса 63\')');
                # results = (session.query(RealtyItem)
                #            .join(RealtyItem.source)
                #            .values(PlayerModel.username,
                #                    MessageModel.message,
                #                    MessageModel.time))

                # query = update(Model).values(field=123)
                # query = query.where(Model.parent_model_id == ParentModel.id)
                # query = query.where(ParentModel.grand_parent_id == GrandParentModel.id)
                # query = query.where(GrandParentModel.name == 'foobar')
                # session.execute(query)

                # users.update().values(name='ed').where(
                #     users.c.name == select([addresses.c.email_address]). \
                #     where(addresses.c.user_id == users.c.id). \
                #     as_scalar()
                # )
                #
                # resultlist = []
                # for username, message, time in results:
                #     resultlist.append({'message': message,
                #                        'username': username,
                #                        'time': time})
                #
                # s.compile(compile_kwargs={"literal_binds": True}))
    session.commit()
    session.close()
# scalar() raises MultipleResultsFound once multiple records found
except MultipleResultsFound as e:
    parser_logger.error("DB broken key violation",err_info=True)

#print(so)
print(r)
print(c)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
# Base.metadata.create_all(engine)
# conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\REALTYDB\realty.accdb;')
# cursor = conn.cursor()
# cursor.execute("SELECT Запись.Торг,Запись.[Дата Подачи] from Запись where cint(Запись.Торг)=-1" )
# cursor.execute("SELECT Запись.[Телефон 1*], Запись.[Цена*1000] from Запись " )
# for row in cursor.fetchall():
#
#       print(*row)
# metadata = MetaData()
# ABase = automap_base(metadata=metadata)
# ABase.prepare(classname_for_table=camelize_classname,
#              name_for_collection_relationship=pluralize_collection
#       )
# # # reflect db schema to MetaData
# metadata.reflect(bind=engine)
# ex_table = metadata.tables['Запись']
# cl = ABase.classes.items()
# print(cl)
# col_num = 1
# columns = [(m.key, m.type) for m in ex_table.columns]
# # types = [col.type for col in ex_table.columns]
# print(*columns, sep='\n')
# while col_num < len(types):
#     try:
#         c = columns[col_num]
#         print(c)
#     except:
#         pass
#     finally:
#         col_num += 1
engine.dispose()
