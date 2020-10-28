import uuid

from crawler_data import CrawlerData
from parser_logger import parser_logger
from selenium.common.exceptions import WebDriverException
# base class for parsing


class Parser:
    driver = None
    download_manager = None
    db_manager = None
    msa = None

    def __init__(self):
        raise Exception("Parser.__init__ Not Implemented")

    # prepares the driver and the environment
    def setup(self):
        raise Exception("Parser.setup Not Implemented")

    # parses the geolocation
    def parse_location(self, location):
        raise Exception("Parser.parse_location Not Implemented")

    def run_parser_task(self, tasks, dw_manager, db_manager):
        # launch managers for input
        if dw_manager is None or db_manager is None:
            parser_logger.error("Avito parser needs dw_manager, db_manager  objects initiated: None passed  ")
            raise ValueError
        self.download_manager = dw_manager
        self.download_manager.begin_downloads()
        self.db_manager = db_manager
        self.db_manager.begin_db_sync()
        for keys, locs in tasks.items():
            print(keys)
            parser_logger.info(keys)
            print(*locs)
            for location in locs:
                try:
                    print(location)
                    parser_logger.info(location)
                    self.setup()
                    self.parse_location(location)
                except ValueError:
                    parser_logger.error("Parser object is broken .", exc_info=True)
                    self.save_scrshot_to_temp()
                except WebDriverException:
                    parser_logger.error("Web driver crashed.", exc_info=True)
                    self.save_scrshot_to_temp()
                except Exception as e:
                    parser_logger.error("Parser crashed.", exc_info=True)
                    self.save_scrshot_to_temp()
                finally:
                    self.dispose()

    def save_scrshot_to_temp(self):
        tmp = CrawlerData.SCR_SHOT_PATH + str(uuid.uuid4()) + ".png"
        parser_logger.info("Screenshot {0}".format(tmp))
        el = self.driver.find_element_by_tag_name('body')
        el.screenshot(tmp)

    def dispose(self):
        # gracefully closing the driver
        parser_logger.info("Closing all active windows. Disposing the driver.")
        self.driver.quit()
        parser_logger.info("Parsing completed.")
