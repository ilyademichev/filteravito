from datetime import time
from locators_realty_item import  Locators
from crawler_data import CrawlerData
from base_page_class import BasePage
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
import logging


class AvitoFilterPage(BasePage):
    """loads filtered realty items page sorted by date"""

    # loads the filter page through driver
    # by given location
    # throws ValueError once the driver is too slow in loading
    # throws WebDriverException on internal webdriver error
    def __init__(self, driver, location):
        super().__init__(driver)
        self.timeout_int = CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS
        self.page_loaded = False
        attempts = 0
        # set geolocation
        link = CrawlerData.SORTED_ITEMS_LOCATION_LINK.replace(CrawlerData.LOCATION_TAG, location)
        while attempts < CrawlerData.ATTEMPTS_INT and not self.page_loaded:
            try:
                driver.get(link)
            # possible slow proxy response
            # double the implicit timeout
            except TimeoutException as errt:
                logging.error("TimeoutException", exc_info=True)
                self.timeout_int = 2 * self.timeout_int
                driver.set_page_load_timeout(self.timeout_int)
                attempts = attempts + 1
                logging.info('Tried: ', attempts, ' out of: ', CrawlerData.ATTEMPTS_INT)
                logging.info('Timeout doubled: ', self.timeout_int, ' s for link:', link)
            #
            except WebDriverException as errw:
                logging.error("WebDriverException", exc_info=True)
                # possible slow proxy response
                if 'Reached error page' in str(errw):
                    attempts = attempts + 1
                    logging.info('Tried ', attempts, ' out of ', CrawlerData.ATTEMPTS_INT)
                # otherwise some webdriver internal exception
                # pass it through to the caller
                else:
                    raise errw
            finally:
                if super().wait_for_js_and_jquery_to_load(self):
                    self.page_loaded = True
        # constructor failed:
        # bad driver with too slow proxy or proxy has gone down.
        # set proper constants in CrawlerData class to adjust the behaviour
        #    IMPLICIT_TIMEOUT_INT_SECONDS
        #    ATTEMPTS_INT
        if not self.phone_popup_loaded:
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


    def scroll_till_loadmore_button_present(self):
        # we feed in the cycle with the timestamps that have been already loaded
        try:
            timestamp = self.driver.find_elements_by_xpath(Locators.TIMESTAMP_DIV)
            ls = list(map(lambda x: x.text, timestamp))
            allday = False
            scrolldown = True
            self.load_more_button_present = super().is_enabled(Locators.LOAD_MORE_SPAN)
            # timestamp of the last item is set
            while not allday and  self.load_more_button_present:
                t = split_timestamps(ls)
            # get day tags and make up  a set
                days = [*map(lambda x: x[0], t)]
                uniquedays = set(days)
                if CrawlerData.STOP_TAG in uniquedays:
                # eliminate the ads
                if days[-1] == CrawlerData.STOP_TAG and days[-2] == CrawlerData.STOP_TAG:
                    allday = True
                    scrolldown = False
                if scrolldown:
                # click a button to expand the list
                    attempts = 0
                    self.page_loaded = False
                    loadmorebutton = None
                    while attempts < CrawlerData.ATTEMPTS_INT and not self.page_loaded:
                        try:
                            loadmorebutton = self.driver.find_element_by_xpath(Locators.LOAD_MORE_SPAN)
                        except NoSuchElementException as errnoel:
                            attempts = attempts + 1
                            logging.error("No click more button error:", errnoel)
                            logging.info('Tried ', attempts, ' out of ', CrawlerData.ATTEMPTS_INT)
                            logging.info("Wait for more time :" , CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS , " s")
                            time.sleep(CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS)
                        finally:
                            self.page_loaded = super().wait_for_js_and_jquery_to_load()
                        try:
                            super().click(Locators.LOAD_MORE_SPAN)
                        except Exception as nobutton:
                            logging.error("No click more button appeared after ", attempts, " tries.", )
                            logging.error("Output of the web site exceeded.")
                    # failed to wait for the page to load and the button to appear
                    # go on processing timetamps
                            break
                #                    raise SystemExit(nobutton)
                    timestamp = self.driver.find_elements_by_xpath(Locators.TIMESTAMP_DIV)
                    logging.info("timestamps found: ", len(timestamp))
                    ls = list(map(lambda x: x.text, timestamp))

    # splits the string list of timestamps into tuple list ( day ,time )
    # timestamps_list : list of timestamps in string format
    def split_timestamps(timestamps_list):
        t = tuple()
        tp = list()
        for ts in timestamps_list:
            m = re.match(r'(?P<day>^.*), (?P<timestamp>\d{2}:\d{2})', ts)
            if m:
                t = (m.group('day'), m.group('timestamp'))
                #            print(t)
                tp.append(t)
        return tp
