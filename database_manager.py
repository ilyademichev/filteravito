import urllib
from threading import Thread
from sqlalchemy import create_engine
import pyodbc
from sqlalchemy.ext.automap import automap_base

from MSACCESSAttachmentLoader import MSA_attachment_loader

connection_string = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    # r'UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;'
    # r'PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL=MS Access;'
    # r'DriverId=25;DefaultDir=C:\REALTYDB;'
    r'DBQ=C:\REALTYDB\realty.accdb;'
    r'ExtendedAnsiSQL=1')
# engine = create_engine(connection_string)
connection_url = f"access+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}"

from threading import Thread
from queue import Queue
import binascii
import logging


class DatabaseSynchronizer:
    def __init__(self, queue , msaccess_com):
        Thread.__init__( self, name=binascii.hexlify(os.urandom(16)) )
        self.queue = queue
        self.msa = msaccess_com


    def run(self):
        while True:
            # gets the realty item from the queue
            realty = self.queue.get()
            logging.info("* Thread {0} - syncing db".format(self.name))
            if not self.sync_database(realty):
                logging.error("* Thread {0} - syncing failed ".format(self.name))
            # send a signal to the queue that the job is done
            self.queue.task_done()

    def sync_database(self, realty_item):
        with lock:
            try:
                session = create_session(bind=engine)
                r = RealtyItem()
                rap = RealtyApartmentPage()
                c = Company()
                r.company_id = realty_item
                # r.rooms
                # r.address
                # r.floor
                # r.s_property
                # r.s_land
                # r.phone
                c = session.query(Company).filter_by(company_name=rap.company)
                r = session.query(Rooms).filter_by(description=rap.rooms)
                st = session.query(RealtyStatus).filter_by(status="в Продаже")
                so = session.query(AdvertismentSource).filter_by(source="")
                q = session.query(RealtyItem).filter_by(company_id=2).all()
                session.close()
                # write images
                self.msa.launch_macro(CrawlerData.MSACCESS_IMPORT_IMAGES_MACRO)
            except:


    class DatabaseManager:
        def __init__(self, download_dict=None, thread_count=1):
            self.download_dict = download_dict
            self.thread_count = thread_count
            self.msa = MSA_attachment_loader()
            self.engine = create_engine(connection_url)
            metadata = MetaData(bind=engine)
            ABase = automap_base(metadata=metadata)
            ABase.prepare()
            metadata.reflect(bind=engine)

        def begin_db_sync(self):
            """
            Start the downloader threads
            """
            self.queue = Queue()
            # Create a thread pool and give them a queue
            for i in range(self.thread_count):
                t = DatabaseSynchronizer(self.queue, msaccess)
                t.setDaemon(False)
                t.start()
            return

        def queue_realties(self, download_dict):
            """
            fill the queue with realties
            """
            self.download_dict = download_dict
            # Load the queue from the download dict
            for adv in self.download_dict:
                self.queue.put(adv)
            return

        # wait for the queue to finish
        # close db connection
        def endup_db_sync(self):
            logging.info("Waiting for  db sync  to complete")
            self.queue.join()
            self.engine.dispose()
            self.msa.dispose()
            return


