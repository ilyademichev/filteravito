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
    avito_output_exceeded = None
    allday = None

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
            # evaluating capcha if needed
            if self.check_for_captcha():
                logging.warning("On requesting avito filter page Captcha is displayed")
                super().save_scrshot_to_temp()
                # try to resolve
                if not self.resolve_captcha():
                    raise ValueError
        # constructor failed:
        # bad driver with too slow proxy or proxy has gone down.
        # set proper constants in CrawlerData class to adjust the behaviour
        #    IMPLICIT_TIMEOUT_INT_SECONDS - timeout of the driver
        #    ATTEMPTS_INT - num of tries
        # press button show for sale only
        if super().is_enabled(Locators.APPARTMENT_SPAN):
            super().click(Locators.APPARTMENT_SPAN)
            if super().wait_for_js_and_jquery_to_load():
                self.page_loaded = True
            else:
                self.page_loaded = False
                raise ValueError
        # no button present - page not fully loaded
        # constructor failed
        else:
            raise ValueError

    # scroll down the page till the yesterdays' mark is not present
    # to discover daily listing of ads

    @property
    def scroll_down(self):
        # Get scroll height
        self.avito_output_exceeded = False
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # check for output
            self.parse_timestamps()
            if CrawlerData.YESTERDAY_TAG in self.uniquedays:
                if self.days[-1] != CrawlerData.TODAY_TAG and self.days[-2] != CrawlerData.TODAY_TAG \
                        and self.days[-3] != CrawlerData.TODAY_TAG:
                    self.allday = True
                    break

            # Scroll down to bottom
            logging.info("Filter page: scrolling down  ")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to scroll the page
            time.sleep(CrawlerData.SCROLL_PAUSE_TIME)
            if not super().wait_for_js_and_jquery_to_load():
                logging.info("Filter page: page can not be fully loaded")
                return False

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            # Check for message from avito no more ads can be displayed
            els = self.driver.find_elements(*Locators.AVITO_OUTPUT_EXCEEDED_DIV)
            if len(els) > 0:
                if els[0].is_displayed():
                    self.avito_output_exceeded = True
                    break

            if new_height == last_height:
                break
            last_height = new_height
        if self.avito_output_exceeded:
            logging.error("Filter page: Avito doesn't send more ads.")
            return False
        else:
            return True

    def parse_timestamps(self):
        timestamp = self.driver.find_elements(*Locators.TIMESTAMP_FILTER_DIV)
        logging.info("Filter page: Timestamps found: {num_timestamps}".format(num_timestamps=len(timestamp)))
        ls = list(map(lambda x: x.text, timestamp))
        t = self.split_timestamps(ls)
        # get day tags and make up a set
        self.days = [*map(lambda x: x[0], t)]
        self.uniquedays = set(self.days)

    def scroll_day(self):
        try:
            # scroll without show more button
            if not self.scroll_down:
                return False
            # if daily output reached
            if self.allday:
                return True
            # otherwise scroll pressing show more button
            el = self.driver.find_elements(*Locators.LOAD_MORE_SPAN)
            if len(el) > 0:
                load_more_button_present = True
            else:
                load_more_button_present = False
            # we feed in the cycle with the timestamps that have been already loaded

            scrolldown = True
            self.avito_output_exceeded = False
            while not self.allday and load_more_button_present:
                # self.days list is filled with timestamps after complete scroll down
                self.parse_timestamps()
                if CrawlerData.YESTERDAY_TAG in self.uniquedays:
                    # SCROLL STOP CRITERIA
                    # We scroll the mobile version of avito.ru
                    # The problem is that realty posts are mixed up with promoted advertisments.
                    # To eliminate the ads we check timestamps. We put them into the list
                    # and check the tail of it ,specifically we check three tail days. For example (...,
                    # ADV_SOME_DATE_TAG,YESTERDAY_TAG,YESTERDAY_TAG)  means that we skipped ads and  reached yesterday's
                    # realty post. We don't have today tags any more. It could present only in ads
                    # i.e. we crawled the whole day period or we get some more output (due to paginated avito output)
                    #
                    # for criteria we must have 3 items
                    # one we have less we put extra empty items to go through criteria in any case
                    while len(self.days) < 3:
                        self.days.append('')
                    if self.days[-1] != CrawlerData.TODAY_TAG and self.days[-2] != CrawlerData.TODAY_TAG and self.days[
                        -3] != CrawlerData.TODAY_TAG:
                        self.allday = True
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
                                # emulate user scroll
                                if not self.scroll_down:
                                    return False
                                # Check for message from avito no more ads can be displayed
                                els = self.driver.find_elements(*Locators.AVITO_OUTPUT_EXCEEDED_DIV)
                                if len(els) > 0:
                                    if els[0].is_displayed():
                                        self.avito_output_exceeded = True
                                        logging.error("Filter page: Avito doesn't send more ads.")
                                        return False
                                self.page_loaded = super().wait_for_js_and_jquery_to_load()
                            else:
                                logging.info("Filter page: No click more button appeared after ", self.attempts,
                                             " tries.", )
                                logging.info("Filter page: Output of the avito filter page exceeded.")
                                # failed to wait for the page to load and the button to appear
                                # go on processing timetamps
                                load_more_button_present = False
                        except Exception as e:
                            self.bad_proxy_connection(e)
            if self.allday:
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
            # regexp samples
            # Вчера, 15:19 day=Вчера timestamp= 15:19
            # Сегодня, 8:43 day=Сегодня timestamp= 8:43
            m = re.match(r'(?P<day>^.*), (?P<timestamp>\d{1,2}:\d{2})', ts)
            if m:
                t = (m.group('day'), m.group('timestamp'))
                #            print(t)
                tp.append(t)
        return tp

    #
    def parse_filter_page(self):
        self.allday = False
        if self.scroll_day():
            realtylinks = self.driver.find_elements(*Locators.APPARTMENT_A)
            self.daily_hrefs = list(map(lambda x: x.get_attribute('href'), realtylinks))
        else:
            logging.info("Filter page: Unable to load daily output.")
            raise ValueError
