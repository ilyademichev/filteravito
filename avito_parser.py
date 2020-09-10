import random
import datetime
import re
import time

import selenium
from selenium.common.exceptions import WebDriverException
import userAgenetRotator
from avito_filter_page import AvitoFilterPage
from crawler_data import CrawlerData
from geolocation_data import geolocation_map
from image_download_manager import DownloadManager
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
# DownloadManager

# DAL ORM classes
# RealtyItem
# Company
# Rooms
# RealtyStatus
# AdvertismentSource

class AvitoParser:
    driver = None
    download_manager = None

    def __init__(self):
        try:
            self.setup_driver()
        except Exception as e:
            logging.error("Parser constructor error.", exc_info=True)
            raise e

    # generate a random UA with environment properties
    def setup_driver(self):
        useragent = random.choice(userAgenetRotator.USER_AGENTS_LIST)
        logging.info(useragent)
        #avoid loading side resources
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
        # hide automation - set random UA
        profile.set_preference("general.useragent.override", useragent)
        options = Options()
        #options.headless = False
        options.headless = True
        driver = Firefox(options=options, firefox_profile=profile, desired_capabilities=caps)
        driver.set_page_load_timeout(CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS)
        self.driver = driver

    # parses the given location into realty_page objects
    # feeds up the image downloader with realty page images

    def parse_location(self, location):
        filter_page = AvitoFilterPage(self.driver, geolocation_map[location])
        filter_page.parse_filter_page()
        # some advertisments found
        if len(filter_page.daily_hrefs) > 0:
            # set up the downloader
            self.download_manager = DownloadManager(thread_count=4)
            self.download_manager.begin_downloads()
            # go through each page sequentially
            for realty_link in filter_page.daily_hrefs:
                realty_page = RealtyApartmentPage(self.driver, realty_link)
                realty_page.parse_realty_apprment_page()
                # extract advertisment number
                # Объявление: №507307470, Сегодня, 14:04
                # make up a tuple of (507307470, {links})
                # queue it up in the image downloader
                # 507307470 will be the folder with links
                adv = [(realty_page.realty_adv_avito_number,imgl) for imgl in realty_page.realty_images]
                self.download_manager.queue_image_links(adv)
        else:
            logging.info("No realty links parsed")

    # feed the parser with  algorithm
    def run_parser_task(self, tasks):
        for keys, locs in tasks.items():
            print(keys)
            logging.info(keys)
            print(*locs)
            for l in locs:
                try:
                    print(l)
                    logging.info(l)
                    self.setup_driver()
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
        # gracefully closing the driver
        logging.info("Closing all active windows. Disposing the driver.")
        self.driver.quit()
        logging.info("Parsing completed.")

    #BAL
    def
        # class Parser:
        #     def

        # BA layer
        r = RealtyItem()

        # r.company_id
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
        ret = Session.query(exists().where(RealtyItem.field == value)).scalar()

        async rap = RealtyApartmentPage(url)
        async rap.parse
        #if the folder exists put into database
        while watch_for_new_files() critical ( putimages() , deletefolter(rap.realty_adv_avito_number) )
        wait for parse
            if session.query(User.query.filter(User.id == 1).exists()).scalar():
                #update, no images
                session.commit()
            else
                #insert
                session.commit()
                #queue images
                #dowload into temp folder, once completed move into main
                rap.download(rap.realty_adv_avito_number)



            if exist(Ri)
            db.update(ri)
            else
            db.insert(ri)
            ri.queueimages
