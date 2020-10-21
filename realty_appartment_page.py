#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import re
from crawler_data import CrawlerData
from locators_realty_item import Locators
from base_page_class import BasePage
import logging


class RealtyApartmentPage(BasePage):
    """loads  realty item page """
    phone_popup_loaded = None
    realty_images = list()
    realty_adv_avito_number = None
    realty_hyperlink = None
    # data fields
    address = None
    area = None
    company = None
    contact_name = None
    description = None
    price = None
    rooms = None
    timestamp = None
    phone = None
    floor = None
    #data field used to store images by the same name

    # throws WebDriverException on internal webdriver error
    def __init__(self, driver, realty_link):
        super().__init__(driver, CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS)
        self.realty_hyperlink = realty_link
        self.load_page()

    def load_page(self):
        self.page_loaded = False
        self.attempts = 0
        # get realty item page
        while self.attempts < CrawlerData.ATTEMPTS_INT and not self.page_loaded:
            try:
                logging.info("Item page request: (URL) {0}".format(self.realty_hyperlink))
                self.driver.get(self.realty_hyperlink)
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

            # by-passing capchas and pop-ups
            if super().check_for_captcha():
                logging.warning("Item page request: Captcha is displayed.")
                super().save_scrshot_to_temp()
                if not self.resolve_captcha():
                    logging.info("Item page request: Captcha is not resolved.")
            if super().check_for_poll_popup():
                logging.warning("Item page request: Poll Pop-up is displayed")
                super().save_scrshot_to_temp()
                if not super().resolve_poll_popup():
                    logging.info("Item page request: Poll Pop-up is not resolved.")
            # expired adv - realty page is invalid and has no relevant data
            if self.check_for_expired_ad():
                logging.warning("Item page request: Advertisment has expired.")

        if not self.page_loaded:
            super().save_scrshot_to_temp()
            raise ValueError

    # Объявление снято с публикации
    def check_for_expired_ad(self):
        els = self.driver.find_elements(*Locators.EXPIRED_ADV_SPAN)
        if len(els) > 0:
            return True
        else:
            return False

    # raises WebDriverException on internal driver error
    # raises ValueError if unable to load the phone window
    # returns:
    #  True if phone button exist - valid page structure
    #  False if not - invalid page structure
    def display_phone_popup(self):
        # initial check for existance of the phone button
        els = self.driver.find_elements(*Locators.PHONE_POPUP_SHOW_LINK)
        if len(els) > 0:
            self.phone_popup_loaded = False
            self.attempts = 0
            while self.attempts < CrawlerData.ATTEMPTS_INT and not self.phone_popup_loaded:
                try:
                    logging.info('Item page parsing: Clicking phone link.')
                    self.click(Locators.PHONE_POPUP_SHOW_LINK)
                    # fully load the phone popup page
                    # if not fully loaded TimeoutException occurs and
                    # further on we utilize slow connection adaptation strategy
                    if super().is_enabled(Locators.PHONE_TEXT):
                        self.phone_popup_loaded = True

                except Exception as e:
                    # possible slow proxy response
                    # double the implicit timeout
                    # fully reload the page
                    self.bad_proxy_connection(e)
                    self.load_page()


                # too slow proxy or proxy has gone down.
                # set proper constants in CrawlerData to adjust the behaviour
                #    IMPLICIT_TIMEOUT_INT_SECONDS
                #    ATTEMPTS_INT
        # no phone button at all : possibly the structure of the page is broken
        else:
            logging.warning("Item Page parsing: Page structure could be broken - phone pop-up link locator not found:")
            return False
        # we reached max number of attempts and failed to load the page
        if not self.phone_popup_loaded:
            logging.warning("Item page parsing: Maximum number of attempts reached while loading the phone pop-up: {0}".format(CrawlerData.ATTEMPTS_INT))
            return False
        else:
            return True

    #

    def parse_phone(self):
        if self.display_phone_popup():
            logging.info('Item page parsing: Fetching the phone number')
            phone = self.driver.find_element(*Locators.PHONE_TEXT).text
        else:
            logging.warning("Item page parsing: Unable to display phone pop-up.")
            return None


    # check for presence of an element given by loc location
    # location loc is the tuple
    # extract and return the text value of the element
    # return None if the element is not present

    def get_text_if_exist(self, loc):
        els = self.driver.find_elements(*loc)
        if len(els) > 0:
            return els[0].text
        else:
            return None

    # parse the currently loaded page
    def parse_realty_apprment_page(self):
        logging.info("Item page parsing: (URL) {0}".format(self.driver.current_url))
        # once there's no adv ID the structure of the page is broken and we skip further processing
        self.timestamp = self.get_text_if_exist(Locators.TIMESTAMP_ITEM_DIV)
        # 9 or more digits for advertisment number
        pattern = re.search('\d{9,}', self.timestamp)
        if not pattern is None:
            self.realty_adv_avito_number = pattern[0]
        else:
            logging.warning("Item page parsing: Page structure is broken: no ID is found.")
            return False
        if not self.parse_realty_images_links():
            logging.warning("Item page parsing: Page structure could be broken: no image links are found.")
        # parse the fields except the phone
        # since the phone popup covers the fields
        self.address = self.get_text_if_exist(Locators.ADDRESS_SPAN)
        self.area = self.get_text_if_exist(Locators.AREA_SPAN)
        self.company = self.get_text_if_exist(Locators.COMPANY_SPAN)
        self.contact_name = self.get_text_if_exist(Locators.CONTACT_NAME_SPAN)
        self.description = self.get_text_if_exist(Locators.DESCRIPTION_SPAN)
        self.price = self.get_text_if_exist(Locators.PRICE_SPAN)
        self.rooms = self.get_text_if_exist(Locators.NUMOF_ROOMS_SPAN)
        self.floor = self.get_text_if_exist(Locators.TIMESTAMP_ITEM_DIV)
        # ocassionally we need to reload the page to get the number
        # the phone button is unclickable
        # so we fetch the phone in the end
        self.phone = self.parse_phone()
        # list out all parsed fields
        logging.info(r"\n".join(r"%s: %s " % item for item in vars(self).items()))
        return True


    # extracts all links to  640x480 images and makes up a proper URL links
    def parse_realty_images_links(self):
        # images by the size 640x480
        pat = re.compile(r"\d{2}\.img\.avito\.st\%2F640x480\%2F\d{10}.jpg")
        # images_div = self.driver.find_elements(*Locators.IMAGES_CONTAINER_SCRIPT)
        # res = pat.findall(images_div[0].get_attribute('innerHTML'))
        if not pat is None:
            res = pat.findall(self.driver.page_source)
            # making up a proper link
            self.realty_images = ["http://" + re.sub(r"\%2F", "/", w) for w in res]
            logging.info("Item page parsing: (Image urls 640x480): {0}".format(res))
            return True
        else:
            return False
