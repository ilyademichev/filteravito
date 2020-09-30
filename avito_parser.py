import random
import datetime
import userAgenetRotator
from avito_filter_page import AvitoFilterPage
from base_parser_class import Parser
from crawler_data import CrawlerData
from geolocation_data import geolocation_map
from realty_appartment_page import RealtyApartmentPage
from selenium import webdriver
from selenium.webdriver import Firefox, DesiredCapabilities
from selenium.webdriver.firefox.options import Options
import logging

# log protocol settings
now = datetime.datetime.now()
logname = str(now.strftime('%Y-%m-%dT%H-%M-%S')) + " parser.log"
logging.basicConfig(level=logging.INFO, filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')

# AvitoParser class uses
# RealtyApartmentPage
# AvitoFilterPage

# DAL ORM classes
# RealtyItem
# Company
# Rooms
# RealtyStatus
# AdvertismentSource


class AvitoParser(Parser):
    def __init__(self):
        super(AvitoParser, self).__init__()
    #
    # setup depends on web-site crawler defense mechanism
    # for avito.ru we generate a random UA with environment settings
    #

    def setup(self):
        useragent = random.choice(userAgenetRotator.USER_AGENTS_LIST)
        logging.info(useragent)
        # avoid loading extra resources
        caps = DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "normal"  # complete
        # caps["pageLoadStrategy"] = "eager"  #  interactive
        # caps["pageLoadStrategy"] = "none"
        # proxy set manually by firefox in a profile folders
        # load the profile with a set proxy
        # profile = webdriver.FirefoxProfile(CrawlerData.FF_PROFILE_PATH)
        # no proxy
        profile = webdriver.FirefoxProfile()
        # no images
        profile.set_preference('permissions.default.image', 2)
        # no flash
        profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        # hide automation - set fake UA
        profile.set_preference("general.useragent.override", useragent)
        options = Options()
        # options.headless = False
        options.headless = True
        driver = Firefox(options=options, firefox_profile=profile, desired_capabilities=caps)
        driver.set_page_load_timeout(CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS)
        self.driver = driver

    # parses the given location into realty_page objects
    # feeds up the db manager with realty page
    def parse_location(self, location):
        filter_page = AvitoFilterPage(self.driver, geolocation_map[location])
        filter_page.parse_filter_page()
        # some advertisments found
        if len(filter_page.daily_hrefs) > 0:
            # go through each page sequentially
            for realty_link in filter_page.daily_hrefs:
                realty_page = RealtyApartmentPage(self.driver, realty_link)
                realty_page.parse_realty_apprment_page()
                self.db_manager.queue_realties(realty_page)

        else:
            logging.info("No realty links parsed")

    # feed the parser with algorithm
    def run_parser_task(self, tasks, dw_manager, db_manager):
        logging.info("avito.ru parsing started.")
        super(AvitoParser, self).run_parser_task(tasks, dw_manager, db_manager)
        logging.info("avito.ru parsing completed.")

    # clean up
    def dispose(self):
        super(AvitoParser, self).dispose()
