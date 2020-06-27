from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from crawler_data import CrawlerData
import logging


class BasePage:
    """This class is the parent class for all the pages in our application."""
    """It contains all common elements and functionalities available to all pages."""
    driver = None
    timeout_int = None
    attempts = None
    page_loaded = None

    def bad_proxy_connection(self,exception):
        # possible slow proxy or network response
        if type(exception).__name__ == 'TimeoutException':
            self.on_exception_prepare_page_reload()
        if type(exception).__name__ == 'WebDriverException':
            logging.error("WebDriverException", exc_info=True)
            #  slow proxy response
            if 'Reached error page' in str(exception.args):
                self.on_exception_prepare_page_reload()
                # reload the page
            # otherwise some webdriver internal exception
            # pass it through to the caller
            # return from the constructor
            else:
                raise exception

    def on_exception_prepare_page_reload(self):
        logging.error("Connection problem", exc_info=True)
        self.timeout_int = 2 * self.timeout_int
        self.driver.set_page_load_timeout(self.timeout_int)
        self.attempts = self.attempts + 1
        logging.info('Tried: ', self.attempts, ' out of: ', CrawlerData.ATTEMPTS_INT)
        logging.info('Timeout doubled: ', self.timeout_int, ' s ')
        self.page_loaded = False

    # this function is called every time a new object of the base class is created.
    def __init__(self, driver, timeout=10):
        self.timeout_int = timeout
        self.driver = driver

    # the wait object for js and jquery
    def wait_for_js_and_jquery_to_load(self):
        # wait for jQuery to load
        class jQueryLoad(object):
            def __init__(self):
                pass

            def __call__(self,driver):
                try:
                    return driver.execute_script("return jQuery.active") == 0
                except Exception as e:
                    # no jQuery present
                    return True

        # wait for Javascript to load
        class jsLoad(object):
            def __init__(self):
                pass

            def __call__(self,driver):
                return driver.execute_script("return document.readyState") == "complete"

        wait = WebDriverWait(self.driver, self.timeout_int)
        return wait.until(jQueryLoad()) and wait.until(jsLoad())

    # this function performs click on web element whose locator is passed to it.
    def click(self, by_locator):
        WebDriverWait(self.driver, self.timeout_int).until(EC.visibility_of_element_located(by_locator)).click()

    # this function checks if the web element whose locator has been passed to it, is enabled or not and returns
    # web element if it is enabled.
    def is_enabled(self, by_locator):
        return WebDriverWait(self.driver, self.timeout_int).until(EC.visibility_of_element_located(by_locator))

    # this function checks if the web element whose locator has been passed to it, is visible or not and returns
    # true or false depending upon its visibility.
    def is_visible(self, by_locator):
        element = WebDriverWait(self.driver, self.timeout_int).until(EC.visibility_of_element_located(by_locator))
        return bool(element)

    # this function moves the mouse pointer over a web element whose locator has been passed to it.
    def hover_to(self, by_locator):
        element = WebDriverWait(self.driver, self.timeout_int).until(EC.visibility_of_element_located(by_locator))
        ActionChains(self.driver).move_to_element(element).perform()
