import os
import threading
import urllib
from sqlalchemy import create_engine, exists, MetaData
import pyodbc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import create_session
from MSACCESSAttachmentLoader import MSA_attachment_loader
from threading import Thread
from queue import Queue
import binascii
import logging
from crawler_data import CrawlerData
from realty_db import RealtyItem, Company, Rooms, RealtyStatus, AdvertismentSource
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
class DatabaseSynchronizerMSA:
    download_manager = None
    engine = None
    name = None #thread name

    def __init__(self,engine, queue ,download_manager):
        """  thread initiation """
        self.engine = engine
        self.queue = queue         #realties queue
        self.download_manager = download_manager
        #thread for database CRUD business logic
        Thread.__init__( self, name=binascii.hexlify(os.urandom(16)) )
        #protect CRUD operations against thread-racing
        self.lock = threading.Lock()

    def run(self):
        """  thread queue cycle """
        while True:
            # gets the realty item from the queue
            realty = self.queue.get()
            logging.info("* Thread {0} - syncing db".format(self.name))
            if not self.sync_database(realty):
                logging.error("* Thread {0} - syncing failed ".format(self.name))
            # send a signal to the queue that the job is done
            self.queue.task_done()

    def sync_database(self, realty_item):
        """  BAL business access logic"""
        #CRUD operations for MS ACCESS are single-user
        #lock is for safety
        with self.lock:
            try:
                #transaction covered by ORM session
                session = create_session(bind=self.engine)
                #ORM operations on DB
                #get adjacent data from linked tables
                c = session.query(Company).filter_by(company_name=realty_item.company)
                r = session.query(Rooms).filter_by(description=realty_item.rooms)
                st = session.query(RealtyStatus).filter_by(status="в Продаже")
                so = session.query(AdvertismentSource).filter_by(source="Avito робот")
                #check for existence of a realty item
                q = session.query(exists().where(
                    RealtyItem.phone == realty_item.phone,
                    RealtyItem.company_id == c.id,
                    RealtyItem.rooms == r.id,
                    RealtyItem.address == realty_item.address,
                    RealtyItem.floor == realty_item.floor,
                    RealtyItem.s_property == realty_item.area,
                    #RealtyItem.s_land = "0"
                    RealtyItem.forsale_forrent == st.id)).scalar()
                #key BAL , update or insert
                #no tiem found : insert new  realty item
                if not q:
                    # queue up the image downloader
                    # extract advertisment number
                    # Объявление: №507307470, Сегодня, 14:04
                    # make up a tuple of (507307470, {links})
                    # queue it up in the image downloader
                    # 507307470 will be the folder with links
                    adv = [(realty_item.realty_adv_avito_number, imgl) for imgl in realty_item.realty_images]
                    self.download_manager.queue_image_links(adv)
                    q = RealtyItem(
                        phone=realty_item.phone,
                        company_id=c.id,
                        rooms=r.id,
                        address=realty_item.address,
                        floor=realty_item.floor,
                        s_property=realty_item.area,
                        forsale_forrent=st.id,
                        description=realty_item.description,
                        contact_name=realty_item.contact_name,
                        url = realty_item.realty_hyperlink,
                        source=so.id,
                        timestamp=datetime.datetime.utcnow,
                        call_timestamp=datetime.datetime.utcnow
                    )
                    #price field could be fictious -we go through validation
                    #once invalid price is set to 0
                    try:
                        q.price = str(int(realty_item.price) / 1000)
                    except ValueError:
                        logging.error("Thread {0} - price conversion failed. Set 0 price . RealtyItem:{1}}".format(self.name,realty_item))
                        q.price = str("0")
                    #insert new realty item
                    session.add(q)
                #update realty item
                else:
                    #set current date
                    #set price
                    #set source "Avito робот"
                    q.timestamp = datetime.datetime.utcnow
                    q.price = r.price
                    q.source = so.id
                session.commit()
                #end up the transaction
                session.close()
            except Exception as e:
                self.error = logging.error(
                    "Thread {0} - ORM session failed on RealtyItem:{1}}".format(self.name, realty_item),exc_info=True)

class DatabaseManager:
    """ singleton database manager. """

    download_manager = None #refence to DownloadManager
    download_dict = None #items to proceed
    thread_count = None
    engine = None
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DatabaseManager.__instance == None:
            DatabaseManager()
        return DatabaseManager.__instance

    def __init__(self,download_manager, download_dict=None, thread_count=1):
        """ Virtually private constructor. """
        # singleton pattern logic
        if DatabaseManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseManager.__instance = self
        self.download_manager =download_manager
        self.download_dict = download_dict
        self.thread_count = thread_count
        #initiate the Database Engine
        self.engine = create_engine(connection_url)
        self.lock = threading.Lock()
        metadata = MetaData(bind=self.engine)
        ABase = automap_base(metadata=metadata)
        ABase.prepare()
        metadata.reflect(bind=self.engine)

    def begin_db_sync(self):
        """
        Start CRUD threads
        """
        self.queue = Queue()
        # Create a thread pool and give them a queue
        # optional: for DBA engine with m-thread support
        # for i in range(self.thread_count):
        # for MSA create only one single thread
        t = DatabaseSynchronizerMSA(self.engine,self.queue,self.download_manager)
        t.setDaemon(False)
        t.start()
    def queue_realties(self, realties_dict):
        """
        fill the queue with realties
        """
        for realty in realties_dict:
            self.queue.put(realty)
    def endup_db_sync(self):
        """
               wait for the queue to empty
        """
        logging.info("Waiting for  db sync  to complete")
        self.queue.join()
        #stop the Database Engine
        self.engine.dispose()

    def MSA_image_sync(self):
        """
               write images into MSA
               single-user access to MSA is crucial
        """
        with self.lock():
            self.msa = MSA_attachment_loader()
            self.msa.launch_macro(CrawlerData.MSACCESS_IMPORT_IMAGES_MACRO)
            self.msa.dispose()



