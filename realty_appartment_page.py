#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
import re
from crawler_data import CrawlerData
from locators_realty_item import Locators
from base_page_class import BasePage
import logging


class RealtyApartmentPage(BasePage):
    """loads filtered realty items page sorted by date"""
    phone_popup_loaded = None
    realty_images = list()
    # data
    # throws WebDriverException on internal webdriver error
    def __init__(self, driver, realty_hyperlink):
        super().__init__(driver)
        self.timeout_int = CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS
        self.page_loaded = False
        self.attempts = 0
        # get realty item page
        while self.attempts < CrawlerData.ATTEMPTS_INT and not self.page_loaded:
            try:
                logging.info("Requesting realty item page {0} :", realty_hyperlink)
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
            if self.check_for_captcha():
                logging.warning("On requesting realty item page Captcha is displayed")
                super().save_scrshot_to_temp()
                self.crunch_captcha()
                self.timeout_int += CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS
                self.attempts += 1

        if not self.page_loaded:
            super().save_scrshot_to_temp()
            raise ValueError

    # raises WebDriverException on internal driver error
    # raises ValueError if unable to load the phone window
    # returns:
    #  True if phone button exist - valid page structure
    #  False if not - invalid page structure
    def display_phone_popup(self):
        els = self.driver.find_elements(*Locators.PHONE_POPUP_SHOW_LINK)
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
        try:
            logging.info(self.driver.current_url)
            # parse the fields except the phone
            # since the phone popup covers the fields
            self.address = self.get_text_if_exist(Locators.ADDRESS_SPAN)
            self.area = self.get_text_if_exist(Locators.AREA_SPAN)
            self.company = self.get_text_if_exist(Locators.COMPANY_SPAN)
            self.contact_name = self.get_text_if_exist(Locators.CONTACT_NAME_SPAN)
            self.description = self.get_text_if_exist(Locators.DESCRIPTION_SPAN)
            self.price = self.get_text_if_exist(Locators.PRICE_SPAN)
            self.rooms = self.get_text_if_exist(Locators.NUMOF_ROOMS_SPAN)
            self.timestamp = self.get_text_if_exist(Locators.TIMESTAMP_ITEM_DIV)
            self.phone = self.parse_phone()
            #self.parse_realty_images_links()
            # list out all parsed fields
            logging.info(pprint.pformat(vars(self)))
        except Exception as e:
            self.bad_proxy_connection(e)
            logging.error("Unable to parse data fields", exc_info=True)
            raise ValueError

    def parse_realty_images_links(self):
        imgs = self.driver.find_elements(*Locators.IMAGE_LINK_DIV)
        self.realty_images = [img.get_attribute("src") for img in imgs]
        #
        #images are stored on cdn-servers
        #resolution is set directly in the link
        #for example resolution 75x55 for
        # //60.img.avito.st/75x55/6279872160.jpg
        #we remove heading // and change resolution numbers to 640x480
        #the resultant link is
        # 60.img.avito.st/640x480/6279872266.jpg
        #
        self.realty_images = [re.sub(r"\/\/","",w) for w in self.realty_images]
        self.realty_images = [re.sub(r"\.st\/.*\/",".st/640x480/",w) for w in self.realty_images]

    def check_for_captcha(self):
        els = self.driver.find_elements(Locators.CAPTCHA_INPUT_ID)
        if len(els) > 0:
            return True
        else:
            return False

    def crunch_captcha(self):
        logging.warning("Crunching captcha: pass")
        pass




