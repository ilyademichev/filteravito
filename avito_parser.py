import random
import datetime
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

# log basic steps
now = datetime.datetime.now()
logname = "parser " + str(now.strftime('%Y-%m-%dT%H-%M-%S')) + ".log"
logging.basicConfig(level=logging.INFO, filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S' )
# generate random UA
def setup_driver():
    useragent = random.choice(userAgenetRotator.USER_AGENTS_LIST)
    logging.info(useragent)
    # proxy set manually by firefox in a profile folders
    # load the profile with a set proxy
    profile = webdriver.FirefoxProfile("/home/ilya/.mozilla/firefox/vfwzppqq.avitoproxy")
    # no images
    profile.set_preference('permissions.default.image', 2)
    profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    # set fake UA
    profile.set_preference("general.useragent.override", useragent)
    options = Options()
    options.headless = True
    driver = Firefox(options=options, firefox_profile=profile)
    driver.set_page_load_timeout(CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS)
    return driver

def parse_location(driver,location):
    filter_page = AvitoFilterPage(driver, geolocation_map["Москва"])
    filter_page.parse_filter_page()
    if len(filter_page.daily_hrefs) > 0:
        for realty_link in filter_page.daily_hrefs:
            realty_page = RealtyApartmentPage(driver, realty_link)
            realty_page.parse_realty_apprment_page()
    else:
        logging.info("No links parsed")

tests = {
         #"TEST 1":["Москва", "Москва", "Москва"],
         "TEST 2":["Обнинск","Обнинск","Обнинск"]#,
         #"TEST 3":["Москва", "Обнинск", "Москва", "Обнинск","Москва", "Обнинск"]
         }

for keys,locs in tests.items():
    print (keys)
    logging.info(keys)
    print(*locs)
    for l in locs:
            try:
                d = setup_driver()
                print(l)
                logging.info(l)
                parse_location(d,l)
            except ValueError:
                logging.error("Avito wrapper object is broken.", exc_info=True)
            except WebDriverException:
                logging.error("Web driver crashed.", exc_info=True)
            except Exception:
                logging.error("Parser crashed.", exc_info=True)
            finally:
                logging.info("Closing all active windows. Disposing the driver")
                d.close()
                d.quit()
                logging.info("Parsing completed")
