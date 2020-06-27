import re
import time
from locators_realty_item import Locators
from crawler_data import CrawlerData
from base_page_class import BasePage
import logging


class AvitoFilterPage(BasePage):
    """loads filtered realty items page sorted by date"""
    phone_popup_loaded = None
    days = None
    uniquedays = None
    daily_hrefs = None

    # loads the filter page through driver
    # by given location
    # throws ValueError once the driver is too slow in loading
    # throws WebDriverException on internal webdriver error

    def __init__(self, driver, location):
        self.attempts = 0
        # base class setup
        super().__init__(driver, CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS)
        # self.timeout_int = CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS
        self.page_loaded = False
        # set geolocation
        link = CrawlerData.SORTED_ITEMS_LOCATION_LINK.replace(CrawlerData.LOCATION_TAG, location)
        # load the filter page with ATTEMPTS_INT tries
        while self.attempts < CrawlerData.ATTEMPTS_INT and not self.page_loaded:
            try:
                driver.get(link)
            # possible slow proxy or network response
            except Exception as e:
                self.bad_proxy_connection(e)
                continue
            # while self.attempts < CrawlerData.ATTEMPTS_INT:
            # check for fully loaded  page
            if super().wait_for_js_and_jquery_to_load():
                self.page_loaded = True
        # constructor failed:
        # bad driver with too slow proxy or proxy has gone down.
        # set proper constants in CrawlerData class to adjust the behaviour
        #    IMPLICIT_TIMEOUT_INT_SECONDS - timeout of the driver
        #    ATTEMPTS_INT - num of tries
        if not self.page_loaded:
            raise ValueError

    # scroll down the page till the yesterdays' mark is not present
    # to discover daily listing of ads

    def scroll_down(self):
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(CrawlerData.SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def scroll_day(self):
        try:
            self.scroll_down()
            self.wait_for_js_and_jquery_to_load()
            load_more_button_present = super().is_enabled(Locators.LOAD_MORE_SPAN)
            # we feed in the cycle with the timestamps that have been already loaded
            # cycle flags
            allday = False
            scrolldown = True
            while not allday and load_more_button_present:
                # ls list is filled with timestamps after complete scroll down
                timestamp = self.driver.find_elements(*Locators.TIMESTAMP_FILTER_DIV)
                logging.info("timestamps found: ", len(timestamp))
                ls = list(map(lambda x: x.text, timestamp))
                t = self.split_timestamps(ls)
                # get day tags and make up  a set
                self.days = [*map(lambda x: x[0], t)]
                self.uniquedays = set(self.days)
                if CrawlerData.YESTERDAY_TAG in self.uniquedays:
                    # eliminate the ads
                    # check the tail of the days list
                    # (...,YESTERDAY_TAG,YESTERDAY_TAG)  means that we skipped ads and reached yesterday
                    # i.e. we crawled the whole day period or we get some more (due to paginated avito output)
                    if self.days[-1] == CrawlerData.YESTERDAY_TAG and self.days[-2] == CrawlerData.YESTERDAY_TAG:
                        allday = True
                        scrolldown = False
                if scrolldown:
                    # click a button to expand the list
                    attempts = 0
                    self.page_loaded = False
                    load_more_button_present = None
                    while attempts < CrawlerData.ATTEMPTS_INT and not self.page_loaded:
                        try:
                            if super().is_enabled(Locators.LOAD_MORE_SPAN):
                                load_more_button_present = True
                                super().click(Locators.LOAD_MORE_SPAN)
                                self.scroll_down()
                                self.page_loaded = super().wait_for_js_and_jquery_to_load()
                            else:
                                logging.info("No click more button appeared after ", self.attempts, " tries.", )
                                logging.info("Output of the avito filter page exceeded.")
                                # failed to wait for the page to load and the button to appear
                                # go on processing timetamps
                                load_more_button_present = False
                        except Exception as e:
                            self.bad_proxy_connection(e)
            if allday:
                return True
        except Exception as e:
            self.bad_proxy_connection(e)
            return False
    # splits the string list of timestamps into tuple list ( day ,time )
    # timestamps_list : list of timestamps in string format
    @staticmethod
    def split_timestamps(timestamps_list):
        tp = list()
        for ts in timestamps_list:
            m = re.match(r'(?P<day>^.*), (?P<timestamp>\d{2}:\d{2})', ts)
            if m:
                t = (m.group('day'), m.group('timestamp'))
                #            print(t)
                tp.append(t)
        return tp

    #
    def parse_filter_page(self):
        self.scroll_day()
        realtylinks = self.driver.find_elements(*Locators.APPARTMENT_A)
        self.daily_hrefs = list(map(lambda x: x.get_attribute('href'), realtylinks))
