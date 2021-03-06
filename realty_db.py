# -*- coding: utf-8 -*-
# import urllib
# ORM DAL
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
# Create and engine and get the metadata
# from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy_utils import URLType
# from sqlalchemy. access import Integer
# from sqlalchemy.dialects import registry

# registry.register("access", "sqlalchemy_access.pyodbc", "AccessDialect_pyodbc")
# registry.register("access.pyodbc", "sqlalchemy_access.pyodbc", "AccessDialect_pyodbc")
# mymetadata = MetaData()
# Base = automap_base(metadata=mymetadata)
Base = declarative_base()


# engine = create_engine(connection_string)
class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class RealtyItem(Base):
    __tablename__ = 'Запись'
    # __table__ = Table(__tablename__, metadata, autoload=True,autoload_with=engine)
    # __table__ = init_table('Запись')
    # __mapper_args__ = {
    #     'primary_key': ['Объект*']
    # }
    phone = Column('Телефон 1*', String(255), primary_key=True)
    company_id = Column('Организация*', Integer, ForeignKey('Организации.Код'), primary_key=True)
    rooms = Column('Объект*', Integer, ForeignKey('Число комнат.Код'), primary_key=True)
    address = Column('Адрес', String(255), primary_key=True)
    floor = Column('Этаж*', String(255), primary_key=True)
    street = Column('Ул/пр*', Integer, ForeignKey('Улици.Код'), primary_key=True)
    house_num = Column('№ дома*', String(255), primary_key=True)
    # agent_name=Column('Организация*', Integer, )
    s_property = Column('S общ*/объекта', String(255), primary_key=True)
    # s_land=Column('S уч, сот', String(255), primary_key=True)
    forsale_forrent = Column('Актуальность*', Integer, ForeignKey('Продано, на задатке, не отвечает.Код'),
                             primary_key=True)
    description = Column('Примечание 3', LONGTEXT)
    contact_name = Column('Имя 1', String(255))
    url = Column('Ссылка', URLType)
    price = Column('Цена min*1000', String(255))
    # source=Column('Источник', Integer,ForeignKey('Источники.Код'))
    timestamp = Column('Дата Подачи', DateTime)
    call_timestamp = Column('Дата Прозвона/Преостановлено до/Позвонить', DateTime)
    realty_adv_avito_number = Column('Номер объявления авито', String(255))


class Company(Base):
    __tablename__ = "Организации"
    id = Column('Код', Integer, primary_key=True)
    company_name = Column('Организация', String(255))
    # realty_id = Column(Integer, ForeignKey('users.id'))
    properties = relationship("RealtyItem", backref="Организации",
                              cascade="all, delete, delete-orphan")


class Rooms(Base):
    __tablename__ = "Число комнат"
    id = Column('Код', Integer, primary_key=True)
    description = Column('Объект', Integer, primary_key=True)
    properties = relationship("RealtyItem", backref="Число комнат",
                              cascade="all, delete, delete-orphan")


class RealtyStatus(Base):
    __tablename__ = "Продано, на задатке, не отвечает"
    id = Column('Код', Integer, primary_key=True)
    status = Column('Продано', String(255))
    properties = relationship("RealtyItem", backref="Продано, на задатке, не отвечает",
                              cascade="all, delete, delete-orphan")


# class AdvertismentSource(Base):
#     __tablename__ = "Источники"
#     id = Column('Код', Integer, primary_key=True)
#     source = Column('Источник/Реклама', String(255))
#     properties = relationship("RealtyItem", backref="Источники", \
#                           cascade="all, delete, delete-orphan")

class Streets(Base):
    __tablename__ = "Улици"
    id = Column('Код', Integer, primary_key=True)
    street = Column('Улица', String(255))
    properties = relationship("RealtyItem", backref="Улици",
                              cascade="all, delete, delete-orphan")

class Regions(Base):
    __tablename__ = "Области"
    id = Column ( 'Код', Integer, primary_key=True )
    region = Column ( 'Область', String ( 255 ) )
    # properties = relationship ( "RealtyItem", backref="Улици",
    #                             cascade="all, delete, delete-orphan" )

class RegionalDistrict(Base):
    __tablename__ = "Район"
    id = Column ( 'Код', Integer, primary_key=True )
    district = Column ( 'Область', String ( 255 ) )
    # properties = relationship ( "RealtyItem", backref="Улици",
    #                             cascade="all, delete, delete-orphan" )

class Locality(Base):
    __tablename__ = "Города"
    id = Column ( 'Код', Integer, primary_key=True )
    locality = Column ( 'НП', String ( 255 ) )
    kind = Column ( 'Тип НП', String ( 255 ) )
    #     # properties = relationship ( "RealtyItem", backref="Улици",
    #     #                             cascade="all, delete, delete-orphan" )

class HouseNumber(Base):
    __tablename__ = "Номер дома"
    id = Column ( 'Код', Integer, primary_key=True )
    locality = Column ( 'НП', String ( 255 ) )
    kind = Column ( 'Тип НП', String ( 255 ) )
    #     # properties = relationship ( "RealtyItem", backref="Улици",
    #     #                             cascade="all, delete, delete-orphan" )



# user_table = Table('Запись', metadata,
#             Column('id', Integer, primary_key=True),
#             Column('name', String),
#         )
