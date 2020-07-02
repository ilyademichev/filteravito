from pprint import pprint

from crawler_data import CrawlerData
from locators_realty_item import Locators
from base_page_class import BasePage
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
    # returns:
    #  True if phone button exist - valid page structure
    #  False if not - invalid page structure
    def display_phone_popup(self):
        els = self.driver.find_elements(Locators.PHONE_POPUP_SHOW_LINK)
        if len(els) > 0:
            self.phone_popup_loaded = False
            self.attempts = 0
            while self.attempts < CrawlerData.ATTEMPTS_INT and not self.phone_popup_loaded:
                try:
                    logging.info('Clicking phone link ')
                    self.click(Locators.PHONE_POPUP_SHOW_LINK)
                    # fully load the phone popup page
                    # if not fully loaded TimeoutException occurs and
                    # further on we utilize slow connection adaptation strategy
                    if super().is_enabled(Locators.PHONE_TEXT):
                        self.phone_popup_loaded = True

                except Exception as e:
                    self.bad_proxy_connection(e)
                    continue
                    # possible slow proxy response
                    # double the implicit timeout
                # wait for fully load the page

                # too slow proxy or proxy has gone down.
                # set proper constants in CrawlerData to adjust the behaviour
                #    IMPLICIT_TIMEOUT_INT_SECONDS
                #    ATTEMPTS_INT
        else:
            return False
        if not self.phone_popup_loaded:
            raise ValueError
        else:
            return True

    def parse_phone(self):
        phone = None
        try:
            if self.display_phone_popup():
                logging.info('fetching the phone number')
                phone = self.driver.find_element(*Locators.PHONE_TEXT).text
        except Exception as e:
            self.bad_proxy_connection(e)
        finally:
            return phone

    # check for presence of an element given by loc location
    # extract and return the text value of the element
    # return None if the element is not present
    def get_text_if_exist(self, loc):
        els = self.driver.find_elements(loc)
        if len(els) > 0:
            return els[0].text
        else:
            return None

    # parse the currently loaded page
    def parse_realty_apprment_page(self):
        try:
            logging.info(self.driver.current_url)
            # parse the fields except the phone
            # since the phone popup covers the fields
            self.address = self.get_text_if_exist(*Locators.ADDRESS_SPAN)
            #            self.area = self.get_text_if_exist(*Locators.AREA_SPAN)
            self.company = self.get_text_if_exist(*Locators.COMPANY_SPAN)
            self.contact_name = self.get_text_if_exist(*Locators.CONTACT_NAME_SPAN)
            self.description = self.get_text_if_exist(*Locators.DESCRIPTION_SPAN)
            self.price = self.get_text_if_exist(*Locators.PRICE_SPAN)
            #            self.rooms = self.get_text_if_exist(*Locators.NUMOF_ROOMS_SPAN)
            #            self.timestamp = self.get_text_if_exist(*Locators.TIMESTAMP_ITEM_DIV)
            self.phone = self.parse_phone()
            # list out all parsed fields
            logging.info(pprint(vars(self)))
        except Exception as e:
            self.bad_proxy_connection(e)
            logging.error("Unable to parse data fields", exc_info=True)
            raise ValueError
