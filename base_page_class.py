import uuid

from captcha_solver import CaptchaSolver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# from captcha_decoder import decoder
from crawler_data import CrawlerData
from parser_logger import parser_logger
import time
#captcha-solver 0.1.5
#from captcha_solver import  CaptchaSolver
#Pillow lib for image handling
from PIL import Image
from locators_realty_item import Locators
import pytesseract
import cv2

class BasePage:
    """This class is the parent class for all the pages in our application."""
    """It contains all common elements and functionalities available to all pages."""
    driver = None
    timeout_int = None
    attempts = None
    page_loaded = None
    captcha_fname = None

    def bad_proxy_connection(self,exception):
        # possible slow proxy or network response
        self.save_scrshot_to_temp()
        if type(exception).__name__ == 'TimeoutException':
            self.on_exception_prepare_page_reload()
        if type(exception).__name__ == 'WebDriverException':
            parser_logger.error("WebDriverException", exc_info=True)
            #  slow proxy response
            if 'Reached error page' in str(exception.args):
                time.sleep(CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS)
                self.on_exception_prepare_page_reload()
                # reload the page
            # otherwise some webdriver internal exception
            # pass it through to the caller
            # return from the constructor
            else:
                raise exception

# adaptaiton strategy for slow internet connection
# we double the wait time
# increment the number of tries
    def on_exception_prepare_page_reload(self):
        parser_logger.error("Connection problem", exc_info=True)
        self.timeout_int += CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS
        self.driver.set_page_load_timeout(self.timeout_int)
# cache clearing
#        self.driver.delete_all_cookies()
        self.attempts += 1
        parser_logger.info("Tried: {num_attempts} out of: {all_attempts}".format(num_attempts=self.attempts,all_attempts=CrawlerData.ATTEMPTS_INT))
        parser_logger.info("Timeout: {timeout} s".format(timeout=self.timeout_int))
        self.page_loaded = False

    # this function is called every time a new object of the base class is created.
    def __init__(self, driver, timeout=10):
        self.timeout_int = timeout
        self.driver = driver
        self.driver.set_page_load_timeout(self.timeout_int)

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

    # takes the screenshot of current driver page and saves it to a random file
    def save_scrshot_to_temp(self):
        tmp = CrawlerData.SCR_SHOT_PATH + str(uuid.uuid4()) + ".png"
        parser_logger.info(tmp)
        el = self.driver.find_element_by_tag_name('body')
        el.screenshot(tmp)

    # check for poll pop-up
    def check_for_poll_popup(self):
        els = self.driver.find_elements(*Locators.POLL_POP_UP_DIV)
        if len(els) > 0:
                return True
        else:
            return False
    # close pop-up
    def resolve_poll_popup(self):
        try:
            self.driver.find_element(*Locators.POLL_POP_UP_CLOSECROSS_DIV).click()
        except Exception as e:
            parser_logger.error("Unable to close pop up", exc_info=True)
            return False
        return True

    # check for captcha page
    def check_for_captcha(self):
        els = self.driver.find_elements(*Locators.CAPTCHA_INPUT_ID)
        if len(els) > 0:
            return True
        else:
            return False

    # save image
    def save_captcha_image(self):
        # get image
        els = self.driver.find_elements(*Locators.CAPTCHA_IMG_CLASS)
        cap_img = els[0]
        # getting element's location
        loc1 = cap_img.location
        # getting element's size
        size1 = cap_img.size
        # save page's screenshot
        self.driver.save_screenshot('capcha_page_scrsht.png')
        # open the image using Pillow
        image2 = Image.open('capcha_page_scrsht.png')
        # setting the crop attributes using image's location and size.
        left = loc1['x']
        top = loc1['y']
        right = loc1['x'] + size1['width']
        bottom1 = loc1['y'] + size1['height']
        # crop the image using the attributes defined
        image2 = image2.crop((left, top, right, bottom1))
        # use the attribute to save image
        self.captcha_fname = 'captcha.png'
        image2.save(self.captcha_fname)

    # decodes captcha
    def crunch_captcha_by_rucaptcha(self):
        parser_logger.warning("Crunching captcha with rucaptcha.")
        solver = CaptchaSolver('rucaptcha', api_key='e3b85f77282f434d6fc90c642be8cce7')
        self.save_captcha_image()
        raw_data = open(self.captcha_fname, 'rb').read()
        sol = solver.solve_captcha(raw_data)
        #sol = decoder(captcha_fname,)
        parser_logger.info("CAPTCHA Solved:".format(sol))
        return sol

    def crunch_captcha_by_teserract(self):
        parser_logger.warning("Crunching captcha with teserract.")
        self.save_captcha_image()
        # https://stackoverflow.com/questions/48279667/scrapy-simple-captcha-solving-example
        # remove color
        image = cv2.imread(self.captcha_fname)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # gray = cv2.medianBlur(gray, 3)
        filename = "{}.png".format("temp")
        cv2.imwrite(filename, gray)
        # crunch by pytesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
        sol = pytesseract.image_to_string(Image.open("temp.png"))
        parser_logger.info("CAPTCHA Solved:".format(sol))
        return sol
    #
    def resolve_captcha(self):
            el = self.driver.find_element(*Locators.CAPTCHA_INPUT_ID)
        # try:
        #     s = self.crunch_captcha_by_rucaptcha()
        # except Exception as e:
        #     parser_logger.error("captcha by rucaptcha solver failed")
            try:
                s = self.crunch_captcha_by_teserract()
            except Exception as e:
                parser_logger.error("Resolving captcha by teserract solver failed",   exc_info=True)
                return False
        # send solution
            try:
                el.send_keys(s)
                self.driver.find_element(*Locators.CAPTCHA_BUTTON).click()
            except Exception as e:
                parser_logger.error("Unable to send resolved captcha",exc_info=True)
                return False
            return True
