from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    """This class is the parent class for all the pages in our application."""
    """It contains all common elements and functionalities available to all pages."""

    # this function is called every time a new object of the base class is created.
    def __init__(self, driver, timeout=10):
        self.WAIT_TIMEOUT = timeout
        self.driver = driver

    # the wait object for js and jquery
    def wait_for_js_and_jquery_to_load(self):
        # wait for jQuery to load
        class jQueryLoad:
            def __init__(self, driver):
                self.driver = driver

            def __call__(self):
                try:
                    return self.driver.executeScript("return jQuery.active") == 0
                except Exception as e:
                    # no jQuery present
                    return True

        # wait for Javascript to load
        class jsLoad:
            def __init__(self, driver):
                self.driver = driver

            def __call__(self):
                return self.driver.executeScript("return document.readyState") == "complete"

        wait = WebDriverWait(self.driver, self.WAIT_TIMEOUT)
        return wait.until(jQueryLoad(self.driver)) and wait.until(jsLoad(self.driver))

    # this function performs click on web element whose locator is passed to it.
    def click(self, by_locator):
        WebDriverWait(self.driver, self.WAIT_TIMEOUT).until(EC.visibility_of_element_located(by_locator)).click()

    # this function checks if the web element whose locator has been passed to it, is enabled or not and returns
    # web element if it is enabled.
    def is_enabled(self, by_locator):
        return WebDriverWait(self.driver, self.WAIT_TIMEOUT).until(EC.visibility_of_element_located(by_locator))

    # this function checks if the web element whose locator has been passed to it, is visible or not and returns
    # true or false depending upon its visibility.
    def is_visible(self, by_locator):
        element = WebDriverWait(self.driver, self.WAIT_TIMEOUT).until(EC.visibility_of_element_located(by_locator))
        return bool(element)

    # this function moves the mouse pointer over a web element whose locator has been passed to it.
    def hover_to(self, by_locator):
        element = WebDriverWait(self.driver, self.WAIT_TIMEOUT).until(EC.visibility_of_element_located(by_locator))
        ActionChains(self.driver).move_to_element(element).perform()
