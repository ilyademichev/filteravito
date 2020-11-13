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
    def test_initial_queue(self):
        self.assertIsNotNone(self.DBM.queue)

    def test_initial_DownloadManager(self):
        self.assertIsNotNone(self.DBM.download_manager)

    def test_initial_engine(self):
        self.assertIsNotNone(self.DBM.engine)

# transaction test
class Testsync_database(TestDatabaseSynchronizerMSA):
    # empty RealtyApartmentPage()
    try:
        ria = RealtyApartmentPage()
    except ValueError:
        pass
    f = open("realty_items.txt", "r")
    ls = f.readlines()
    for l in ls:
        key = l.partition(':')[0]
        value = l.partition(':')[1]
        print(key)
        print(value)
    f.close()
    setattr(ria, key, value)



