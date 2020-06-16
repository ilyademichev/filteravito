import TestData
from selenium.common.exceptions import WebDriverException, TimeoutException

from testdata
import logging

class RealtyApartmentPage(BasePage):
    """loads filtered realty items page sorted by date"""
#loads the page through driver
#by given location
#throws ValueError once the driver is too slow in loading
#throws SystemExit on internal webdriver error - fatal  crash
    def __init__(self, driver, location):
        super().__init__(driver)
        self.timeout_int = TestData.IMPLICIT_TIMEOUT_INT_SECONDS
        self.page_loaded = False
        attempts = 1
        link = TestData.SORTED_ITEMS_LOCATION_LINK.replace(TestData.LOCATION_TAG, location)
        while attempts < TestData.ATTEMPTS_INT and not self.page_loaded:
        try:
            #set geolocation
            driver.get(link)
        except WebDriverException as errw:
            logging.error("WebDriverException", exc_info=True)
            logging.info('Tried ', attempts, ' out of ', TestData.ATTEMPTS_INT)
            #possible slow proxy response
            if 'Reached error page' in str(errw):
                attempts = attempts + 1
            #some internal exception
            else:
                raise SystemExit(errw)
        #possible slow proxy response
        except TimeoutException as errt:
            logging.error("TimeoutException", exc_info=True)
            logging.info('Tried: ', attempts, ' out of: ', TestData.ATTEMPTS_INT)
            self.timeout_int = 2 * self.timeout_int
            driver.set_page_load_timeout(self.timeout_int)
            attempts = attempts + 1
            logging.info('Timeout doubled: ', self.timeout_int, ' s for link:' ,link)
        finally:
            page_state = driver.execute_script('return document.readyState;')
            if page_state == 'complete':
                page_loaded = True
        #bad driver with too slow proxy or proxy has gone down.
        #set proper constants in testdata.py to adjust the behaviour
        #    IMPLICIT_TIMEOUT_INT_SECONDS
        #    ATTEMPTS_INT
        if not self.page_loaded :
            raise ValueError

    def search(self):
        self.driver.find_element(*Locators.SEARCH_TEXTBOX).clear()
        self.enter_text(Locators.SEARCH_TEXTBOX, TestData.SEARCH_TERM)
        self.click(Locators.SEARCH_SUBMIT_BUTTON)