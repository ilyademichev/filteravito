from unittest import TestCase
import userAgenetRotator
from avito_filter_page import AvitoFilterPage
from crawler_data import CrawlerData
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox, DesiredCapabilities
from geolocation_data import geolocation_map

class TestAvitoFilterPage(TestCase):
    def create_selenium_driver(self):
        useragent = random.choice(userAgenetRotator.USER_AGENTS_LIST)
        # avoid loading extra resources
        caps = DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "normal"  # complete
        # caps["pageLoadStrategy"] = "eager"  #  interactive
        # caps["pageLoadStrategy"] = "none"
        # proxy set manually by firefox in a profile folders
        # load the profile with a set proxy
        profile = webdriver.FirefoxProfile(CrawlerData.FF_PROFILE_PATH)
        # no proxy
        #profile = webdriver.FirefoxProfile()
        # no images
        # profile.set_preference('permissions.default.image', 2)
        # no flash
        profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        # hide automation - set fake UA
        profile.set_preference("general.useragent.override", useragent)
        options = Options()
        # options.headless = False
        options.headless = True
        driver = Firefox(options=options, firefox_profile=profile, desired_capabilities=caps)
        driver.set_page_load_timeout(CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS)
        self.driver = driver

    def setUp(self):
        self.AFP = AvitoFilterPage(driver=self.create_selenium_driver(),location=geolocation_map["Москва"])

class TestInit(TestAvitoFilterPage):
    def test_initial_driver(self):
        self.assertIsNotNone(self.AFP.driver)

    # def test_initial_timeout_int(self):
    #     self.assertEqual(self.AFP.driver.timeout()  , CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS)

    def test_initial_attempts(self):
        self.assertEqual(self.AFP.attempts, 0)

class TestLoad(TestAvitoFilterPage):
    def test_load_none_location(self):
        self.assertRaises(ValueError, self.AFP.load_page(location=None))

    def test_load_empty_location(self):
        self.assertRaises(ValueError, self.AFP.load_page(location=""))

    def test_load_huge_location(self):
        self.AFP.load_page(geolocation_map["Москва"])
        self.assertTrue(self.AFP.page_loaded)

    def test_load_small_location(self):
        self.AFP.load_page(geolocation_map["Жуков"])
        self.assertTrue(self.AFP.page_loaded)

class TestScroll(TestAvitoFilterPage):
    def test_scroll(self):
        self.AFP.load_page(geolocation_map["Жуков"])
        self.assertTrue(self.AFP.scroll_down())

class TestParseTimeStamps(TestAvitoFilterPage):
    def test_timestamps(self):
        self.AFP.load_page(geolocation_map["Жуков"])
        self.assertTrue(self.AFP.parse_timestamps())

class TestScrollDay(TestAvitoFilterPage):
    def test_block_scroll_day(self):
        self.AFP.load_page(geolocation_map["Жуков"])
        self.assertTrue(self.AFP.scroll_day())

class TestSplit(TestAvitoFilterPage):
    def test_split_timestamps_none(self):
        self.assertEqual(self.AFP.split_timestamps(None),{})

    def test_split_timestamps_wrong_structure(self):
        self.AFP.load_page(geolocation_map["Жуков"])
        garbaged_timestamps = {"15:19, Вчера","Вчера","15:19","фыва","Фыва","1234"}
        self.assertEqual(self.AFP.split_timestamps(garbaged_timestamps), {})

    def test_split_timestamps_right_structure(self):
        timestamps = {"Вчера, 15:19"}
        self.assertEqual(self.AFP.split_timestamps(garbaged_timestamps), {("Вчера","15:19")})





