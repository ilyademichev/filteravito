from crawler_data import CrawlerData
from parserealtyitem import Locators
from basepageclass import BasePage
from selenium.common.exceptions import WebDriverException, TimeoutException
import logging

class RealtyApartmentPage(BasePage):
    """loads filtered realty items page sorted by date"""
#loads the page through driver
#by given location
#throws ValueError once the driver is too slow in loading
#throws WebDriverException on internal webdriver error
    def __init__(self, driver, location):
        super().__init__(driver)
        self.timeout_int = CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS
        self.page_loaded = False
        self.phone_popup_loaded = False
        attempts = 0
        # set geolocation
        link = CrawlerData.SORTED_ITEMS_LOCATION_LINK.replace(CrawlerData.LOCATION_TAG, location)
        while attempts < CrawlerData.ATTEMPTS_INT and not self.phone_popup_loaded:
            try:
                driver.get(link)
            except WebDriverException as errw:
                logging.error("WebDriverException", exc_info=True)
                #possible slow proxy response
                if 'Reached error page' in str(errw):
                    attempts = attempts + 1
                    logging.info('Tried ', attempts, ' out of ', CrawlerData.ATTEMPTS_INT)
                #otherwise some webdriver internal exception
                #pass it through to the caller
                else:
                    raise errw
            #possible slow proxy response
            #double the implicit timeout
            except TimeoutException as errt:
                logging.error("TimeoutException", exc_info=True)
                self.timeout_int = 2 * self.timeout_int
                driver.set_page_load_timeout(self.timeout_int)
                attempts = attempts + 1
                logging.info('Tried: ', attempts, ' out of: ', CrawlerData.ATTEMPTS_INT)
                logging.info('Timeout doubled: ', self.timeout_int, ' s for link:' ,link)
            finally:
                if super().waitForJSandJQueryToLoad(self):
                    self.page_loaded = True
        #constructor failed:
        #bad driver with too slow proxy or proxy has gone down.
        #set proper constants in CrawlerData class to adjust the behaviour
        #    IMPLICIT_TIMEOUT_INT_SECONDS
        #    ATTEMPTS_INT
        if not self.phone_popup_loaded :
            raise ValueError

    def displayPhonePopup(self):
        self.phone_popup_loaded = False
        attempts = 0
        while attempts < CrawlerData.ATTEMPTS_INT and not self.phone_popup_loaded:
            try:
                logging.info('Clicking phone link ',Locators.PHONE_POPUP_SHOW_LINK)
                self.click(Locators.PHONE_POPUP_SHOW_LINK)
            except WebDriverException as errw:
                logging.error("WebDriverException", exc_info=True)
                logging.info('Tried ', attempts, ' out of ', CrawlerData.ATTEMPTS_INT)
                # possible slow proxy response
                if 'Reached error page' in str(errw):
                    attempts = attempts + 1
                # otherwise some webdriver internal exception
                # pass it through to the caller
                else:
                    raise errw
                    # possible slow proxy response
                    # double the implicit timeout
            except TimeoutException as errt:
                logging.error("TimeoutException", exc_info=True)
                self.timeout_int = 2 * self.timeout_int
                self.set_page_load_timeout(self.timeout_int)
                attempts = attempts + 1
                logging.info('Tried: ', attempts, ' out of: ', CrawlerData.ATTEMPTS_INT)
                logging.info('Timeout doubled: ', self.timeout_int, ' s for pressing phone popup link:')
            finally:
                if super().waitForJSandJQueryToLoad(self):
                    self.phone_popup_loaded = True
                # instance is broken
                # return ValueError
                # bad driver with too slow proxy or proxy has gone down.
                # set proper constants in CrawlerData to adjust the behaviour
                #    IMPLICIT_TIMEOUT_INT_SECONDS
                #    ATTEMPTS_INT
            if not self.phone_popup_loaded:
                logging.error("WebDriverException", exc_info=True)
                logging.info('Tried ', attempts, ' out of ', CrawlerData.ATTEMPTS_INT)
                # possible slow proxy response
                if 'Reached error page' in str(errw):
                    attempts = attempts + 1
                # otherwise some webdriver internal exception
                # pass it through to the caller
                else:
                    raise errw
                raise ValueError

    def parse_phone(self):
        phone = None
        try:
            logging.info('fetching the phone number')
            phone = self.driver.find_element(*Locators.PHONE_TEXT).text
        except WebDriverException as errw:
            logging.error("WebDriverException", exc_info=True)
            raise errw
        finally:
            return phone
