import logging

from selenium.common.exceptions import WebDriverException

from database_manager import DatabaseManager
from image_download_manager import DownloadManager


class Parser:
    driver = None
    download_manager = None
    db_manager = None
    msa = None
    def __init__(self):
        try:
            self.setup()
        except Exception as e:
            logging.error("Parser constructor error.", exc_info=True)
            raise e

    def setup(self):
        pass

    def parse_location(self, location):
        pass

    def run_parser_task(self, tasks):
        self.download_manager = DownloadManager(thread_count=4)
        self.download_manager.begin_downloads()
        self.db_manager = DatabaseManager(thread_count=1)
        self.db_manager.begin_db_sync()
        for keys, locs in tasks.items():
            print(keys)
            logging.info(keys)
            print(*locs)
            for l in locs:
                try:
                    print(l)
                    logging.info(l)
                    self.setup()
                    self.parse_location(l)
                except ValueError:
                    logging.error("Avito wrapper object is broken.", exc_info=True)
                except WebDriverException:
                    logging.error("Web driver crashed.", exc_info=True)
                except Exception:
                    logging.error("Parser crashed.", exc_info=True)
                finally:
                    self.dispose()

    def dispose(self):
        # gracefully waiting for picture download  to complete
        if not self.download_manager is None:
            self.download_manager.endup_downloads()
        # gracefully waiting for db operations to complete
        if not self.download_manager is None:
            self.db_manager.endup_db_sync()