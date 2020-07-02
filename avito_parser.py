import random
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import userAgenetRotator
from avito_filter_page import AvitoFilterPage
from crawler_data import CrawlerData
from geolocation_data import geolocation_map
from realty_appartment_page import RealtyApartmentPage
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import logging
#log basic steps
logging.basicConfig(level=logging.INFO)
#generate random UA
useragent = random.choice(userAgenetRotator.USER_AGENTS_LIST)
logging.info(useragent)
#proxy set manually by firefox in a profile folders
#load the profile with a set proxy
profile = webdriver.FirefoxProfile("/home/ilya/.mozilla/firefox/vfwzppqq.avitoproxy")
#no images
profile.set_preference('permissions.default.image', 2)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
# set fake UA
profile.set_preference("general.useragent.override", useragent)
options = Options()
options.headless = True
try:
    driver = Firefox(options=options, firefox_profile=profile)
    driver.set_page_load_timeout(CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS)
    filter_page = AvitoFilterPage(driver, geolocation_map["Обнинск"])
    filter_page.parse_filter_page()
    for realty_link in filter_page.daily_hrefs:
        realty_page = RealtyApartmentPage(driver, realty_link)
        realty_page.parse_realty_apprment_page()
except ValueError:
    logging.error("Avito wrapper object is broken.", exc_info=True)
except WebDriverException:
    logging.error("Web driver crashed.", exc_info=True)
except Exception:
    logging.error("Parser crashed.", exc_info=True)
finally:
    logging.info("Closing all active windows. Disposing the driver")
    driver.close()
    driver.quit()
    logging.info("Parsing completed")




