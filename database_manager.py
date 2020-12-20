import os
import re
import time
import urllib
from sqlalchemy import create_engine
import pyodbc
from sqlalchemy.orm import  sessionmaker, scoped_session
from sqlalchemy.orm.exc import MultipleResultsFound
from MSACCESSAttachmentLoader import MSAttachmentLoader
from threading import Thread, Lock
from queue import Queue
import binascii
from parser_logger import parser_logger
from crawler_data import CrawlerData
from realty_db import RealtyItem, Company, Rooms, RealtyStatus,  Streets # , AdvertismentSource
import datetime
connection_string = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    # r'UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;'
    # r'PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL=MS Access;'
    # r'DriverId=25;DefaultDir=C:\REALTYDB;'
    # r'DBQ=C:\REALTYDB\realty.accdb;'
    r'DBQ=' + CrawlerData.MSACCESS_DB_PATH_WINDOWS + CrawlerData.MSACCESS_DB_FILENAME_WINDOWS + ';'
    r'ExtendedAnsiSQL=1')
# engine = create_engine(connection_string)
connection_url = f"access+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}"
#Singleton for CRUD operations on MS ACCESS DB
#creates DB thread fed from realties queue



class DatabaseSynchronizerMSA(Thread):
    download_manager = None
    engine = None
    Session = None

    def __init__(self, r_queue ,download_manager,addr_decomposer):
        """  thread initiation """
       # self.engine = engine
        if download_manager is None:
            parser_logger.error("* Thread {0} - Download manager object is required ".format(self.name))
            raise ValueError
        if addr_decomposer is None:
            parser_logger.error("* Thread {0} - Address decomposer object is required ".format(self.name))
            raise ValueError

        self.__realties_queue = r_queue         #realties queue
        # self.address_queue = a_queue        #address queue
        self.download_manager = download_manager
        self.address_manager = addr_decomposer
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
            realty = self.__realties_queue.get(block=True,timeout=None)
            parser_logger.info("* Thread {0} - syncing db".format(self.name))
            if not self.sync_database(realty):
                parser_logger.error("* Thread {0} - syncing failed ".format(self.name))
            # send a signal to the queue that the job is done
            self.queue.task_done()

# make price conversion
# input: ri_price of text from RealtyApprtmentPage.price
# output: price /1000 as string
# ValueError : conversion error
    def get_price(self,ri_price):
        try:
            price = re.sub(r"[^\w]", '', ri_price)  # remove spaces
            m = re.match(r"\d+", price)
            if m:
                price = str(int(int(m.group(0)) / 1000))
            else:
                parser_logger.error(
                    "* Thread {0} Wrong price value. Set empty price field  *".format(self.name))
                price = str("")
        except ValueError:
            parser_logger.error("* Thread {0} price conversion failed. Set empty price field  *".format(self.name))
            price = str("")
        return price


    def sync_database(self, realty_item_page):
        """  BAL business access logic"""
        # debug print out of a pending item
        print(', '.join("%s: %s \n" % item for item in vars(realty_item_page).items()))
        # CRUD operations for MS ACCESS are single-user
        # lock is for safety
        with self.lock:
            try:
                #transaction covered by ORM session
                session = self.Session()
                #ORM operations on DB
                # get adjacent data from linked tables
                # MS ACCESS table: "Организации"
                c = session.query(Company).filter_by(company_name=realty_item_page.company).scalar()
                if not c:
                    parser_logger.info("Appending Company")
                    c = Company(company_name=realty_item_page.company)
                    session.add(c)
                # MS ACCESS table: "Число комнат"
                r = session.query(Rooms).filter_by(description=realty_item_page.rooms).scalar()
                if not r:
                    parser_logger.info("Appending Rooms")
                    r = Rooms(description=realty_item_page.rooms)
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
                    phone = re.sub(r"[^\w]", '', realty_item_page.phone) # remove spaces and -
                    phone = phone[1:] if phone.startswith('7') else phone # remove heading 7
                except:
                    parser_logger.error ("* Thread {0} - Phone Conversion Failed {1}".format (
                            self.name, realty_item_page.phone ), exc_info=True )
                q = session.query(RealtyItem).filter_by(
                        realty_adv_avito_number = realty_item_page.realty_adv_avito_number
                        # phone=phone,
                        # company_id=c.id,
                        # rooms=r.id,
                        # address=realty_item_page.address,
                        # floor=realty_item_page.floor,
                        # # street=st.id,
                        # # house_num=house_not_identified,
                        # s_property=realty_item_page.area,
                        # forsale_forrent=stat.id
                ).scalar()
                # quering the address decomposition thread if  the address is parsed
                #if self.address_manager.ready(realty_item_page.realty_adv_avito_number):
                #wait for the address to come
                if not q:
                    parser_logger.info("Appending RealtyItem")
                    # compose new item
                    t = datetime.date.fromtimestamp(time.time())
                    # make up a desktop url out of mobile, remove prefix m.
                    desktop_url = realty_item_page.realty_hyperlink.replace("//m.", "//")
                    # ms access hyperlink format (text to display)#(Target URL)
                    msaccess_desktop_url =  desktop_url + "#" + desktop_url + "#"
                    q = RealtyItem(
                        phone=phone,
                        company_id=c.id,
                        rooms=r.id,
                        address=realty_item_page.address,
                        street=st.id,
                        house_num=house_not_identified,
                        floor=realty_item_page.floor,
                        s_property=realty_item_page.area,
                        forsale_forrent=stat.id,
                        description=realty_item_page.description,
                        contact_name=realty_item_page.contact_name,
                        url=msaccess_desktop_url,
                        # source=so.id,
                        timestamp=t,
                        call_timestamp=t,
                        price=self.get_price(realty_item_page.price),
                        realty_adv_avito_number=realty_item_page.realty_adv_avito_number
                    )
                    # insert new realty item
                    session.add(q)
                    # queue download manager with fresh image links from new item
                    image_folder =CrawlerData.MSACCESS_DB_PATH_WINDOWS + CrawlerData.IMAGE_FOLDER + realty_item_page.realty_adv_avito_number
                    image_queue_dict = [( image_folder, link) for link in realty_item_page.realty_images]
                    self.download_manager.queue_image_links(image_queue_dict)
                    #self.
                else:
                    # refresh the time
                    # set current date
                    # set price
                    # set source "Avito робот"
                    q.call_timestamp = datetime.date.fromtimestamp(time.time())
                    q.price = self.get_price(realty_item_page.price)
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
                parser_logger.error("Thread {0} - ORM session failed on RealtyItem".format(self.name),exc_info=True)
                return False
        return True

class DatabaseManager:
    """ singleton database manager. """
    __instance = None
    # @staticmethod
    # def getInstance():
    #     """ Static access method. """
    #     if DatabaseManager.__instance == None:
    #         DatabaseManager()
    #     return DatabaseManager.__instance
    def __init__(self,download_manager, download_dict=None, thread_count=1):
        """ Virtually private constructor. """
        self.download_manager = None  # refence to DownloadManager
        self.download_dict = None  # items to proceed
        self.thread_count = None
        self.engine = None
        self.__queue = None
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
        self.msa = None
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
        self.__realty_queue = Queue()
        self.__address_queue = Queue()
        # Create a thread pool and give them a queue
        # optional: for DBA engine with m-thread support
        for i in range(self.thread_count):
        # for MSA create only one single thread
            t = DatabaseSynchronizerMSA(self.__realty_queue,self.__address_queue,self.download_manager)
            t.setDaemon(True)
            t.start()
        return

    def queue_realties(self, realties_list):
        """
        fill the queue with realties
        """
        for realty in realties_list:
            self.__realty_queue.put( realty )
        return

    def queue_addresses(self, addresses_list):
        """
            fill the queue with adresses
        """
        for a in addresses_list:
            self.__address_queue.put( a )
        return



    def endup_db_sync(self):
        """
               wait for the queue to empty
        """
        parser_logger.info("Waiting for  db sync  to complete")
        if not self.__queue is None:
            self.__queue.join()
        #stop the Database Engine
        self.engine.dispose()
        return

    def MSA_image_sync(self):
        """
               write images into MSA
               single-user access to MSA is crucial
        """
        # with self.lock:
        try:
            self.msa = MSAttachmentLoader()
            self.msa.launch_macro(CrawlerData.MSACCESS_IMPORT_IMAGES_MACRO)
        except Exception as e:
            parser_logger.error( "MSA COM ERROR ", exc_info=True )
        finally:
            if self.msa is not None:
                self.msa.dispose()
        return

    def get_address_components(self):
        pass



