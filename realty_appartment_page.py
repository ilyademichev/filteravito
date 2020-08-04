#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from crawler_data import CrawlerData
from locators_realty_item import Locators
from base_page_class import BasePage
import logging


class RealtyApartmentPage(BasePage):
    """loads filtered realty items page sorted by date"""
    phone_popup_loaded = None
    realty_images = list()
    realty_adv_avito_number = None
    realty_hyperlink = None

    # data
    # throws WebDriverException on internal webdriver error
    def __init__(self, driver, realty_hyperlink):
        super().__init__(driver)
        self.realty_hyperlink =realty_hyperlink
        self.load_page()

    def load_page(self):
        self.timeout_int = CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS
        self.page_loaded = False
        self.attempts = 0
        # get realty item page
        while self.attempts < CrawlerData.ATTEMPTS_INT and not self.page_loaded:
            try:
                logging.info("Requesting realty item page {0} :".format(realty_hyperlink))
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
            if self.check_for_captcha():
                logging.warning("On requesting realty item page Captcha is displayed")
                super().save_scrshot_to_temp()
                self.resolve_captcha()

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
                    # possible slow proxy response
                    # double the implicit timeout
                    # fully reload the page
                    self.bad_proxy_connection(e)
                    self.load_page()
                    continue


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
            self.realty_adv_avito_number = re.search('\d{10}', self.timestamp)[0]
            self.parse_realty_images_links()
            #ocassionally we need to reload the page to get the number
            #so we fetch the phone in the end
            self.phone = self.parse_phone()

            # list out all parsed fields
            # logging.info(', '.join("%s: %s" % item for item in vars(self).items()))
        except Exception as e:
            self.bad_proxy_connection(e)
            logging.error("Unable to parse data fields", exc_info=True)
            raise ValueError

    # extracts all links to  640x480 images and makes up a proper URL links
    def parse_realty_images_links(self):
        # images by the size 640x480
        pat = re.compile(r"\d{2}\.img\.avito\.st\%2F640x480\%2F\d{10}.jpg")
        # images_div = self.driver.find_elements(*Locators.IMAGES_CONTAINER_SCRIPT)
        # res = pat.findall(images_div[0].get_attribute('innerHTML'))
        res = pat.findall(self.driver.page_source)
        # making up a proper link
        self.realty_images = [ "http://" + re.sub(r"\%2F", "/", w) for w in res]
        logging.info("Image links 640x480:{0}".format(res))
