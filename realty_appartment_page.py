from pprint import pprint

from crawler_data import CrawlerData
from locators_realty_item import Locators
from base_page_class import BasePage
from selenium.common.exceptions import WebDriverException, TimeoutException
import logging


class RealtyApartmentPage(BasePage):
    """loads filtered realty items page sorted by date"""
    phone_popup_loaded = None
    # data
    phone = None
    timestamp = None
    price = None
    address = None
    company = None
    contact_name = None
    description = None
    area = None
    rooms = None

    # loads the page through driver
    # by given location
    # throws ValueError once the driver is too slow in loading
    # throws WebDriverException on internal webdriver error
    def __init__(self, driver, realty_hyperlink):
        super().__init__(driver)
        self.timeout_int = CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS
        self.page_loaded = False
        self.attempts = 0
        # set geolocation
        while self.attempts < CrawlerData.ATTEMPTS_INT and not self.page_loaded:
            try:
                driver.get(realty_hyperlink)
            # possible slow proxy response
            # double the implicit timeout
            except Exception as e:
                self.bad_proxy_connection(e)
                continue
            if super().wait_for_js_and_jquery_to_load():
                self.page_loaded = True
        # constructor failed:
        # bad driver with too slow proxy or proxy has gone down.
        # set proper constants in CrawlerData class to adjust the behaviour
        #    IMPLICIT_TIMEOUT_INT_SECONDS
        #    ATTEMPTS_INT
        if not self.page_loaded:
            raise ValueError

    # raises WebDriverException on internal driver error
    # raises ValueError if unable to load the phone window
    def display_phone_popup(self):
        self.phone_popup_loaded = False
        self.attempts = 0
        while self.attempts < CrawlerData.ATTEMPTS_INT and not self.phone_popup_loaded:
            try:
                logging.info('Clicking phone link ', *Locators.PHONE_POPUP_SHOW_LINK)
                self.click(Locators.PHONE_POPUP_SHOW_LINK)
            except Exception as e:
                self.bad_proxy_connection(e)
                continue
                    # possible slow proxy response
                    # double the implicit timeout
            # wait for fully load the page
            if super().wait_for_js_and_jquery_to_load():
                self.phone_popup_loaded = True
                # too slow proxy or proxy has gone down.
                # set proper constants in CrawlerData to adjust the behaviour
                #    IMPLICIT_TIMEOUT_INT_SECONDS
                #    ATTEMPTS_INT
        if not self.phone_popup_loaded:
            raise ValueError

    def parse_phone(self):
        phone = None
        try:
            logging.info('fetching the phone number')
            phone = self.driver.find_element(*Locators.PHONE_TEXT).text
        except Exception as e:
            self.bad_proxy_connection(e)
        finally:
            return phone

    def parse_realty_apprment_page(self):
        try:
            #parse the fields except the phone
            #since the phone popup covers the fields
            self.address = self.driver.find_element(*Locators.ADDRESS_SPAN).text
            self.area = self.driver.find_element(*Locators.AREA_SPAN).text
            self.company = self.driver.find_element(*Locators.COMPANY_SPAN).text
            self.contact_name = self.driver.find_element(*Locators.CONTACT_NAME_SPAN).text
            self.description = self.driver.find_element(*Locators.DESCRIPTION_SPAN).text
            self.price = self.driver.find_element(*Locators.PRICE_SPAN).text
            self.rooms = self.driver.find_element(*Locators.NUMOF_ROOMS_SPAN).text
            self.timestamp = self.driver.find_element(*Locators.TIMESTAMP_DIV).text
            #make phone popup visible
            self.display_phone_popup()
            self.phone = self.parse_phone()
            #list out all parsed fields
            logging.info(pprint(vars(self)))
        except Exception as e:
            self.bad_proxy_connection(e)
            logging.error("Unable to parse data fields", exc_info=True)
            raise ValueError


