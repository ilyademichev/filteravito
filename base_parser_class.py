import logging
from selenium.common.exceptions import WebDriverException
# base class for parsing

class Parser:
    driver = None
    download_manager = None
    db_manager = None
    msa = None

    def __init__(self):
        raise Exception ("Parser.__init__ Not Implemented")

    # prepares the driver and the environment
    def setup(self):
        raise Exception ("Parser.setup Not Implemented")

    # parses the geolocation
    def parse_location(self, location):
        raise Exception ("Parser.parse_location Not Implemented")

    def run_parser_task(self, tasks, dw_manager, db_manager):
        # launch managers for input
        if dw_manager is None or db_manager is None:
            logging.error("Avito parser needs dw_manager, db_manager  objects initiated: None passed  ")
            raise ValueError
        self.download_manager = dw_manager
        self.download_manager.begin_downloads()
        self.db_manager = db_manager
#        self.db_manager.begin_db_sync()
        for keys, locs in tasks.items():
            print(keys)
            logging.info(keys)
            print(*locs)
            for location in locs:
                try:
                    print(location)
                    logging.info(location)
                    self.setup()
                    self.parse_location(location)

                except ValueError:
                    logging.error("Avito parser is broken .", exc_info=True)
                except WebDriverException:
                    logging.error("Web driver crashed.", exc_info=True)
                except Exception as e:
                    logging.error("Parser crashed.", exc_info=True)
                finally:
                    self.dispose()

    def dispose(self):
        # gracefully closing the driver
        logging.info("Closing all active windows. Disposing the driver.")
        self.driver.quit()
        logging.info("Parsing completed.")

