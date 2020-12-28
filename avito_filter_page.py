import re
import time
from locators_realty_item import Locators
from crawler_data import CrawlerData
from base_page_class import BasePage
from parser_logger import parser_logger


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

    def __init__(self, driver):
        self.attempts = 0
        # base class setup
        super().__init__(driver, CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS)
        # self.timeout_int = CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS
        self.page_loaded = False
        # set geolocation

    def load_page(self, location):
        if location is None or not location:
            parser_logger.error("Avito filter page: load_page arguement of location must not be empty or None ")
            raise ValueError
        link = CrawlerData.SORTED_APPARTMENTS_LOCATION_LINK.replace(CrawlerData.LOCATION_TAG, location)
        # load the filter page with ATTEMPTS_INT tries
        while self.attempts < CrawlerData.ATTEMPTS_INT and not self.page_loaded:
            try:
                self.driver.get(link)
            # possible slow proxy or network response
            except Exception as e:
                self.bad_proxy_connection(e)
                continue
            # while self.attempts < CrawlerData.ATTEMPTS_INT:
            # check for fully loaded  page
            if super().wait_for_js_and_jquery_to_load():
                self.page_loaded = True
            # evaluating capcha if needed
            if super().check_for_blocked_page():
                parser_logger.warning("Avito filter page: Blocking page is displayed")
                super().save_scrshot_to_temp()
                # give more time for loading
                super().bad_proxy_connection()
                # raise ValueError - either wait  1 hour or revolve proxy server
            if super().check_for_server_fail():
                parser_logger.warning("Avito filter page: Server Fail page is displayed")
                super().save_scrshot_to_temp()
                # give more time for loading
                super().bad_proxy_connection()
            if super().check_for_captcha():
                parser_logger.warning("Avito filter page: Captcha is displayed")
                super().save_scrshot_to_temp()
                # try to resolve
                if not self.resolve_captcha():
                    parser_logger.info("Avito filter page: Captcha is not resolved.")
                    raise ValueError
                else:
                    if self.wait_for_js_and_jquery_to_load():
                        self.page_loaded = True
            if super().check_for_poll_popup():
                parser_logger.warning("Avito filter page: Poll Pop-up is displayed")
                super().save_scrshot_to_temp()
                if not super().resolve_poll_popup():
                    raise ValueError
                else:
                    if self.wait_for_js_and_jquery_to_load():
                        self.page_loaded = True
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
            parser_logger.info("Avito filter page: scrolling down  ")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to scroll the page
            time.sleep(CrawlerData.SCROLL_PAUSE_TIME)
            if not super().wait_for_js_and_jquery_to_load():
                parser_logger.info("Avito filter page: page can not be fully loaded")
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
            parser_logger.error("Avito filter page: Avito doesn't send more ads.")
            return False
        else:
            return True

    def parse_timestamps(self):
        timestamp = self.driver.find_elements(*Locators.TIMESTAMP_FILTER_DIV)
        if len(timestamp) > 0:
            parser_logger.info("Avito filter page: Timestamps found: {num_timestamps}".format(num_timestamps=len(timestamp)))
            ls = list(map(lambda x: x.text, timestamp))
            t = self.split_timestamps(ls)
            # get day tags and make up a set
            self.days = [*map(lambda x: x[0], t)]
            self.uniquedays = set(self.days)
            return True
        else:
            return False

    def scroll_day(self):
        try:
            # scroll without show more button
            if not self.scroll_down():
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
                    # once we have less we put extra empty items to go through criteria in any case
                    while len(self.days) < 3:
                        self.days.append('')
                    # SCROLL STOP CRITERIA :
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
                                if not self.scroll_down():
                                    return False
                                # Check for message from avito no more ads can be displayed
                                els = self.driver.find_elements(*Locators.AVITO_OUTPUT_EXCEEDED_DIV)
                                if len(els) > 0:
                                    if els[0].is_displayed():
                                        self.avito_output_exceeded = True
                                        parser_logger.error("Avito filter page: Avito doesn't send more ads.")
                                        return False
                                self.page_loaded = super().wait_for_js_and_jquery_to_load()
                            else:
                                parser_logger.info("Avito filter page: No click more button appeared after ",
                                                   self.attempts,
                                                    " tries.", )
                                parser_logger.info("Avito filter page: Output of the avito filter page exceeded.")
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
            # some delay for occasional page reload
            if not super().wait_for_js_and_jquery_to_load():
                parser_logger.info("Avito filter page: page can not be fully loaded.")
                return False
            realtylinks = self.driver.find_elements(*Locators.APPARTMENT_A)
            if len(realtylinks) == 0:
                parser_logger.warning("Avito filter page: No realty links found. Possibly the structure of fileter page is broken.")
                return False
            self.daily_hrefs = list(map(lambda x: x.get_attribute('href'), realtylinks))
            return True
        else:
            parser_logger.info("Avito filter page: Unable to load daily output.")
            return  False
