#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from selenium.webdriver import ActionChains

from crawler_data import CrawlerData
from locators_realty_item import Locators
from base_page_class import BasePage
from parser_logger import parser_logger


class RealtyApartmentPage(BasePage):
    """loads  realty item page """

    #data field used to store images by the same name

    # throws WebDriverException on internal webdriver error
    def __init__(self, driver, realty_link):
        super().__init__(driver, CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS)
        # popup with mobile phone is diplayed
        self.phone_popup_loaded = None
        # image links
        self.realty_images = None
        # advertisment number as on the realty item page
        self.realty_adv_avito_number = None
        # url link of the realty item
        # data fields
        self.realty_hyperlink = None
        self.address = None
        self.area = None
        self.company = None
        self.contact_name = None
        self.description = None
        self.price = None
        self.rooms = None
        self.timestamp = None
        self.phone = None
        self.floor = None
        # initializing some attributes
        self.realty_images = list()
        # load the realty item Web-page by given URL
        self.realty_hyperlink = realty_link
        self.load_page()

    def load_page(self):
        self.page_loaded = False
        self.attempts = 0
        # get realty item page
        while self.attempts < CrawlerData.ATTEMPTS_INT and not self.page_loaded:
            try:
                parser_logger.info("Item page request: (URL) {0}".format(self.realty_hyperlink))
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
                parser_logger.warning("Item page request: Captcha is displayed.")
                super().save_scrshot_to_temp()
                if not self.resolve_captcha():
                    parser_logger.info("Item page request: Captcha is not resolved.")
            if super().check_for_poll_popup():
                parser_logger.warning("Item page request: Poll Pop-up is displayed")
                super().save_scrshot_to_temp()
                if not super().resolve_poll_popup():
                    parser_logger.info("Item page request: Poll Pop-up is not resolved.")
            # expired adv - realty page is invalid and has no relevant data
            if self.check_for_expired_ad():
                parser_logger.warning("Item page request: Advertisment has expired.")

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
                    parser_logger.info('Item page parsing: Clicking phone link.')
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
            parser_logger.warning("Item Page parsing: Page structure could be broken - phone pop-up link locator not found:")
            return False
        # we reached max number of attempts and failed to load the page
        if not self.phone_popup_loaded:
            parser_logger.warning("Item page parsing: Maximum number of attempts reached while loading the phone pop-up: {0}".format(CrawlerData.ATTEMPTS_INT))
            return False
        else:
            return True

    #

    def parse_phone(self):
        if self.display_phone_popup():
            parser_logger.info('Item page parsing: Fetching the phone number')
            return self.driver.find_element(*Locators.PHONE_TEXT).text
        else:
            parser_logger.warning("Item page parsing: Unable to display phone pop-up.")
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

    def get_text_if_exist_from_li(self,loc):
        els = self.driver.find_elements(*loc)
        if len(els) > 0:
            # remove heading text , leave the data
            child = els[0].find_element_by_tag_name('span')
            els[0].text.replace(child.text,'')
            return els[0].text
        else:
            return None


    # parse the currently loaded page
    def parse_realty_apprment_page(self):
        area_empty_value = '-'
        floor_empty_value = '-'
        parser_logger.info("Item page parsing: (URL) {0}".format(self.driver.current_url))
        # once there's no adv ID the structure of the page is broken and we skip further processing
        self.timestamp = self.get_text_if_exist(Locators.TIMESTAMP_ITEM_DIV)
        # 9 or more digits for advertisment number
        pattern = re.search('\d{9,}', self.timestamp)
        if not pattern is None:
            self.realty_adv_avito_number = pattern[0]
        else:
            parser_logger.warning("Item page parsing: Page structure is broken: no ID is found.")
            return False
        if not self.parse_realty_images_links():
            parser_logger.warning("Item page parsing: Page structure could be broken: no image links are found.")
        # parse the fields except the phone
        # since the phone popup covers the fields
        self.address = self.get_text_if_exist(Locators.ADDRESS_SPAN)
        # area
        # 58 м²
        # \d+([.]\d+)
        # area could be living or total
        # living area checked first
        # once no area found , area set to area_empty_value
        a = self.get_text_if_exist(Locators.AREA_LIVING_DIV)
        if a is None:
            a = self.get_text_if_exist(Locators.AREA_TOTAL_DIV)
        if a is None:
                a = area_empty_value
        else:
            p = re.search(r'\d+([.]\d+)?', a)
            if not p is None:
                self.area = p[0]
            else:
                parser_logger.warning("Item page parsing: Page structure could be broken: no Area is found. Set Area is set to area_empty_value={0}".format(area_empty_value))
                a = area_empty_value
        self.company = self.get_text_if_exist(Locators.COMPANY_SPAN)
        self.contact_name = self.get_text_if_exist(Locators.CONTACT_NAME_SPAN)
        self.description = self.get_text_if_exist(Locators.DESCRIPTION_SPAN)
        self.price = self.get_text_if_exist(Locators.PRICE_SPAN)
        self.rooms = self.get_text_if_exist(Locators.NUMOF_ROOMS_DIV)
        # floor
        # 24 из 52
        # (\d{1,2})
        # try to parse floor if not found then set to floor_empty_value
        p = re.findall(r"(\d+) из (\d+)",  self.get_text_if_exist(Locators.FLOOR_DIV))
        if not p is None:
            self.floor, max_floor = p[0]
        else:
            parser_logger.warning("Item page parsing: Page structure is broken: no Floor is found.")
            self.floor = floor_empty_value
        # ocassionally we need to reload the page to get the number
        # the phone button is unclickable
        # so we fetch the phone in the end
        self.phone = self.parse_phone()
        # list out all parsed fields
        parser_logger.info(u"\n".join(u"%s: %s " % item for item in vars(self).items()))
        return True


    # extracts all links to  640x480 images and makes up a proper URL links
    def parse_realty_images_links(self):
        # first way of getting images from JS script directly
        # images by the size 640x480
        images_parsed_first = False
        images_parsed_second = False
        pat = re.compile(r"\d{2}\.img\.avito\.st\%2F640x480\%2F\d{10}.jpg")
        # images_div = self.driver.find_elements(*Locators.IMAGES_CONTAINER_SCRIPT)
        # res = pat.findall(images_div[0].get_attribute('innerHTML'))
        if not pat is None:
            res = pat.findall(self.driver.page_source)
            if not res:
                images_parsed_first = False
            else:
            # making up a proper link
                self.realty_images = ["http://" + re.sub(r"\%2F", "/", w) for w in res]
                parser_logger.info("Item page parsing: (Image urls 640x480): {0}".format(res))
                images_parsed_first = True
        else:
            raise ValueError("Pattern for image search not compiled.")
        # second way of getting images from elementtiming="bx.gallery"

        els = self.driver.find_elements( *Locators.IMAGES_LINK_elementtiming )
        if len ( els ) > 0 :
            # slide images right to left in image gallery in order for all the images to display
            # locate the slider
            slider_el = self.driver.find_element ()
            # enumerate elements in a slider
            num_of_images = self.driver.find_elements ()
            action = ActionChains ( self.driver )
            for _ in num_of_images :
                # center the mouse on the image
                action.move_by_offset ()
                # fix the mouse button for a slide
                action.click_and_hold ()
                # slide the image gallery by one item
                action.move_by_offset ()
                # wait for image to  fully load
                super ().wait_for_js_and_jquery_to_load ()
            # all images are loaded into the list , parse them into the page
            for e in els :
                self.realty_images.append ( e.get_attribute ( "src" ) )
            images_parsed_second = True
        else :
            images_parsed_second = False

        return ( images_parsed_first or images_parsed_second )




