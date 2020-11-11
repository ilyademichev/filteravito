import os
import re
import time
import urllib
from sqlalchemy import create_engine
import pyodbc
from sqlalchemy.orm import create_session, sessionmaker, scoped_session
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from MSACCESSAttachmentLoader import MSAttachmentLoader
from threading import Thread, Lock
from queue import Queue
import binascii
from parser_logger import parser_logger
from crawler_data import CrawlerData
from realty_db import RealtyItem, Company, Rooms, RealtyStatus,  Base, Streets # , AdvertismentSource
import datetime
connection_string = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    # r'UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;'
    # r'PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL=MS Access;'
    # r'DriverId=25;DefaultDir=C:\REALTYDB;'
    r'DBQ=C:\REALTYDB\realty.accdb;'
    r'ExtendedAnsiSQL=1')
# engine = create_engine(connection_string)
connection_url = f"access+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}"
#Singleton for CRUD operations on MS ACCESS DB
#creates DB thread fed from realties queue


class DatabaseSynchronizerMSA(Thread):
    download_manager = None
    engine = None
    Session = None

    def __init__(self, queue ,download_manager):
        """  thread initiation """
       # self.engine = engine
        self.queue = queue         #realties queue
        self.download_manager = download_manager
        self.engine = create_engine(connection_url, echo=True)
        session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(session_factory)
        #thread for database CRUD business logic
        Thread.__init__( self ,name=binascii.hexlify(os.urandom(16)))
        #protect CRUD operations against thread-racing
        self.lock = Lock()

    def run(self):
        """  thread queue cycle """
        while True:
            # gets the realty item from the queue
            realty = self.queue.get(block=True,timeout=None)
            parser_logger.info("* Thread {0} - syncing db".format(self.name))
            if not self.sync_database(realty):
                parser_logger.error("* Thread {0} - syncing failed ".format(self.name))
            # send a signal to the queue that the job is done
            self.queue.task_done()


    def sync_database(self, realty_item):
        """  BAL business access logic"""
        # debug print out of a pending item
        print(', '.join("%s: %s \n" % item for item in vars(realty_item).items()))
        # CRUD operations for MS ACCESS are single-user
        # lock is for safety
        with self.lock:
            try:
                #transaction covered by ORM session
                session = self.Session()
                #ORM operations on DB
                # get adjacent data from linked tables
                # MS ACCESS table: "Организации"
                c = session.query(Company).filter_by(company_name=realty_item.company).scalar()
                if not c:
                    parser_logger.info("Appending Company")
                    c = Company(company_name=realty_item.company)
                    session.add(c)
                # MS ACCESS table: "Число комнат"
                r = session.query(Rooms).filter_by(description=realty_item.rooms).scalar()
                if not r:
                    parser_logger.info("Appending Rooms")
                    r = Rooms(description=realty_item.rooms)
                    session.add(r)
                # MS ACCESS table: "Продано, на задатке, не отвечает"
                stat = session.query(RealtyStatus).filter_by(status="в Продаже").scalar()
                if not stat:
                    parser_logger.error("* Thread {0} - Required record not found: possibly DB structure is broken {1}".format(self.name, "status='в Продаже'"),exc_info=True)
                # MS ACCESS table: "Источники"
                # so = session.query(AdvertismentSource).filter_by(source="Avito робот").scalar()
                # MS ACCESS table: "Улици"
                # we use full-address and set separate address fields to not identified
                # street not identified
                st = session.query(Streets).filter_by(street="-").scalar()
                if not st:
                    parser_logger.error("* Thread {0} - Required record not found: possibly DB structure is broken {1}".format(self.name, "street='-'"), exc_info=True)
                # house not identified
                house_not_identified = '-'
                #       #check for existence of a realty item
                # unable to use nested queries in ms access and exists statement
                # q = session.query( exists().where(and_(
                #                     RealtyItem.phone == realty_item.phone,
                #                     RealtyItem.company_id == realty_item.company_id,
                #                     RealtyItem.rooms == realty_item.rooms,
                #                     RealtyItem.address == realty_item.address,
                #                     RealtyItem.floor == realty_item.floor,
                #                     RealtyItem.s_property == realty_item.area,
                #                     RealtyItem.forsale_forrent == realty_item.forsale_forrent))).scalar()
                # once multiple items exist MultipleResultsFound raised - compound primary key violation
                try:
                    phone = re.sub(r"[^\w]", '', realty_item.phone) # remove spaces and -
                    phone = phone[1:] if phone.startswith('7') else phone # remove heading 7
                except:
                    pass
                session.commit()
                q = session.query(RealtyItem).filter_by(
                        phone=phone,
                        company_id=c.id,
                        rooms=r.id,
                        address=realty_item.address,
                        floor=realty_item.floor,
                        s_property=realty_item.area,
                        forsale_forrent=stat.id).scalar()
                if not q:
                    parser_logger.info("Appending RealtyItem")
                    # compose new item
                    t = datetime.date.fromtimestamp(time.time())
                    q = RealtyItem(
                        phone=phone,
                        company_id=c.id,
                        rooms=r.id,
                        address=realty_item.address,
                        street=st.id,
                        house_num=house_not_identified,
                        floor=realty_item.floor,
                        s_property=realty_item.area,
                        forsale_forrent=stat.id,
                        description=realty_item.description,
                        contact_name=realty_item.contact_name,
                        url=realty_item.realty_hyperlink,
                        # source=so.id,
                        timestamp=t,
                        call_timestamp=t
                    )
                    try:
                        q.price = str(int(int(realty_item.price) / 1000))
                    except ValueError:
                        parser_logger.error("* Thread {0} price conversion failed. Set empty price field  *".format(self.name))
                        q.price = str("")
                    # insert new realty item
                    session.add(q)
                else:
                    # refresh the time
                    # set current date
                    # set price
                    # set source "Avito робот"
                    q.timestamp = datetime.date.fromtimestamp(time.time())
                    try:
                        q.price = str(int(int(realty_item.price) / 1000))
                    except ValueError:
                        parser_logger.error("* Thread {0} price conversion failed. Set empty price field  *".format(self.name))
                        q.price = str("")

                    # rs = engine.connect().execute('INSERT INTO Запись ( Объект*.Value ) \
                    # VALUES("Avito робот") WHERE Запись.Объект* In (SELECT Запись.Объект* FROM Источники INNER JOIN Запись \
                    # ON Источники.Источник/Реклама = Запись.Объект*) AND Запись.Адрес=г. Обнинск, ул. Шацкого 13 ;')
                    # update realty item
                session.commit()
                self.Session.remove()
                # scalar() raises MultipleResultsFound once multiple records found
            except MultipleResultsFound as e:
                parser_logger.error("* Thread {0} multiple realty items found by complex primary key".format(self.name), err_info=True)
                return False
            except Exception as e:
                parser_logger.error("Thread {0} - ORM session failed on RealtyItem:{1}".format(self.name, realty_item),exc_info=True)
                return False
        return True

class DatabaseManager:
    """ singleton database manager. """

    download_manager = None #refence to DownloadManager
    download_dict = None #items to proceed
    thread_count = None
    engine = None
    __instance = None
    queue = None

    # @staticmethod
    # def getInstance():
    #     """ Static access method. """
    #     if DatabaseManager.__instance == None:
    #         DatabaseManager()
    #     return DatabaseManager.__instance

    def __init__(self,download_manager, download_dict=None, thread_count=1):
        """ Virtually private constructor. """
        # singleton pattern logic
        if DatabaseManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseManager.__instance = self
        self.download_manager = download_manager
        self.download_dict = download_dict
        self.thread_count = thread_count
        #initiate the Database Engine
        self.engine = create_engine(connection_url, echo=True)
        self.lock = Lock()
        # mediate orm doamin models with  db tables
        #Base.metadata.create_all(self.engine, checkfirst=False)
        # Base.prepare(self.engine, reflect=True)
        #Base.metadata.reflect(self.engine,reflect=True)
        #ABase = automap_base(metadata=metadata)
        #ABase.prepare()
        #metadata.reflect(bind=self.engine)


    def begin_db_sync(self):
        """
        Start CRUD threads
        """
        self.queue = Queue()
        # Create a thread pool and give them a queue
        # optional: for DBA engine with m-thread support
        for i in range(self.thread_count):
        # for MSA create only one single thread
            t = DatabaseSynchronizerMSA(self.queue,self.download_manager)
            t.setDaemon(True)
            t.start()
        return

    def queue_realties(self, realties_list):
        """
        fill the queue with realties
        """
        for realty in realties_list:
            self.queue.put(realty)
        return

    def endup_db_sync(self):
        """
               wait for the queue to empty
        """
        parser_logger.info("Waiting for  db sync  to complete")
        if not self.queue is None:
            self.queue.join()
        #stop the Database Engine
        self.engine.dispose()
        return

    def MSA_image_sync(self):
        """
               write images into MSA
               single-user access to MSA is crucial
        """
        with self.lock:
            self.msa = MSAttachmentLoader()
            self.msa.launch_macro(CrawlerData.MSACCESS_IMPORT_IMAGES_MACRO)
            self.msa.dispose()
        return



