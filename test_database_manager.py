from unittest import TestCase
from queue import Queue
from database_manager import DatabaseSynchronizerMSA
from image_download_manager import DownloadManager
from realty_appartment_page import RealtyApartmentPage


class TestDatabaseSynchronizerMSA(TestCase):
    def setUp(self):
        q = Queue()
        dm = DownloadManager()
        self.DBM = DatabaseSynchronizerMSA(q,dm)

class TestInit(TestDatabaseSynchronizerMSA):
    def test_initial_queue(self):
        self.assertIsNotNone(self.DBM.queue)

    def test_initial_DownloadManager(self):
        self.assertIsNotNone(self.DBM.download_manager)

    def test_initial_engine(self):
        self.assertIsNotNone(self.DBM.engine)


class TestRun(TestDatabaseSynchronizerMSA):
    def generate_queue_from_file(self,fname):
        # empty RealtyApartmentPage()
        try:
            ria = RealtyApartmentPage()
        except ValueError:
            pass
        try:
            f = open(fname, "r")
            ls = f.readlines()
            for l in ls:
                key = l.partition(':')[0]
                value = l.partition(':')[1]
                print(key)
                print(value)
                setattr(ria, key, value)
            f.close()
        except IOError as e:
            print(e)
            return False
        return True

    def test_empty_queue(self):
        self.DBM.queue = []
        try:
           self.DBM.run()
        except Exception as e:
           self.fail(msg="Run method with empty queue fails")

    def test_some_queue(self):
        f = "realty_items.txt"
        if self.generate_queue_from_file(f):
           try:
               self.DBM.run()
           except Exception as e:
               self.fail(msg="Run method with several queue items fails")
        else:
           self.fail(msg="Cannot load realty items from: {0}".format(f))



# transaction test
class Test_sync_database(TestDatabaseSynchronizerMSA):
    def generate_one_realty_item(self):
        # empty RealtyApartmentPage()
        try:
            realty_item = RealtyApartmentPage()
        except ValueError:
            pass
        realty_item.phone = "903810488"
        realty_item.address = "г. Обнинск, ул. Маркса 63"
        realty_item.floor = "8"
        realty_item.area = "49"
        realty_item.price = "3900000"
        return realty_item

    def test_transaction_company(self):
        ri =self.generate_one_realty_item()
        # MS ACCESS test set existing
        ri.company = "TEST COMPANY"
        try:
            self.DBM.sync_database(ri)
        except Exception as e:
            self.fail(msg="Run method with several queue items fails")

    def test_transaction_no_company(self):
        # not exisiting company
        ri =self.generate_one_realty_item()
        # MS ACCESS test set: not existing
        ri.company = "NO COMPANY"
        try:
            self.DBM.sync_database(ri)
        except Exception as e:
            self.fail(msg="Run method with several queue items fails")

