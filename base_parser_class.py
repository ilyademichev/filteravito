import logging
from selenium.common.exceptions import WebDriverException
#base class for parsing
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
    #prepares the driver and the environment
    def setup(self):
        pass
    #parses the geolocation
    def parse_location(self, location):
        pass
    #
    def run_parser_task(self, tasks ,dw_manager, db_manager):
        #launch managers for input
        self.download_manager = dw_manager
        self.download_manager.begin_downloads()
        self.db_manager = db_manager
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
                    pass

    def dispose(self):
        # gracefully closing the driver
        logging.info("Closing all active windows. Disposing the driver.")
        self.driver.quit()
        logging.info("Parsing completed.")


