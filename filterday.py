import sys
from multiprocessing import Pool, cpu_count
import tempfile
import re
import time
import random
from selenium import webdriver
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.options import Options
#exceptions handled here
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
#rotator libs
import userAgenetRotator
#agregating the ads timestamps
from itertools import groupby

def run_parallel_selenium_singlecore(datalist, selenium_func):
    pool = Pool()
    for i in range(0, len(datalist) - 1):
        try:
            pool.apply_async(selenium_func, [datalist[i]])
        except Exception as e:
            print(e)


def run_parallel_selenium_processes(datalist, selenium_func):

    pool = Pool()

    # max number of parallel process
    ITERATION_COUNT = cpu_count()-1

    count_per_iteration = len(datalist) / float(ITERATION_COUNT)

    for i in range(0, ITERATION_COUNT):
        list_start = int(count_per_iteration * i)
        list_end = int(count_per_iteration * (i+1))
        pool.apply_async(selenium_func, [datalist[list_start:list_end]])

def parse_realty_page(realty_link):
    useragent = random.choice(userAgenetRotator.USER_AGENTS_LIST)
    profile = webdriver.FirefoxProfile("/home/ilya/.mozilla/firefox/vfwzppqq.avitoproxy")  # asdf
    # no images
    profile.set_preference('permissions.default.image', 2)
    profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    # set fake UA
    profile.set_preference("general.useragent.override", useragent)
    options = Options()
    options.headless = True
    driver = Firefox(options=options, firefox_profile=profile)
    timeout_int = 300
    driver.set_page_load_timeout(timeout_int)
    attempts = 0
    attempts_int = 3
    page_loaded = False
    while attempts < attempts_int and not page_loaded:
        try:
            driver.get(realty_link)
        except WebDriverException as errw:
            print('Tried ', attempts, ' out of ', attempts_int)
            print("WebDriverException", errw)
            if 'Reached error page' in str(errw):
                attempts = attempts + 1
            else:
                raise SystemExit(errw)
        except TimeoutException as errt:
            print('Tried ', attempts, ' out of ', attempts_int)
            print("Timeout Error:", errt)
            timeout_int = 2 * timeout_int
            driver.set_page_load_timeout(timeout_int)
            attempts = attempts + 1
            print('Timeout doubled ', timeout_int)
        finally:
            page_state = driver.execute_script('return document.readyState;')
            if page_state == 'complete':
                page_loaded = True
    scrshotpath = '/home/ilya/scrshotavito'
    tmp = scrshotpath + tempfile.NamedTemporaryFile().name + ".png"
    print(tmp)
    driver.get_screenshot_as_file(tmp)
    driver.quit()

#frequencies of consequetive  occurencies in a list
def freq_consecutive_duplicates(ls_str):
    return [(key, sum(1 for i in group)) for key, group in groupby(ls_str)]
#fake UA
#useragent = 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36'
useragent = random.choice(userAgenetRotator.USER_AGENTS_LIST)

#scrennshot of  a fully loaded page last screen after scrolling
scrshotpath = '/home/ilya/scrshotavito'
# https_proxy_domain = "93.159.236.30"
# https_proxy_port = "8080"
# https_proxy = https_proxy_domain + ":" + https_proxy_port
profile = webdriver.FirefoxProfile("/home/ilya/.mozilla/firefox/vfwzppqq.avitoproxy")#asdf
#locations
#https://www.avito.ru/maloyaroslavets/nedvizhimost?s=104
#https://www.avito.ru/obninsk/nedvizhimost?s=104
#sankt_peterburg_i_lo
sortedItemsLocationLink = 'https://m.avito.ru/obninsk/nedvizhimost?s=104'
# proxy server settings

# webdriver.DesiredCapabilities.FIREFOX['proxy']={
#     "httpProxy":https_proxy,
#     "ftpProxy":https_proxy,
#     "sslProxy":https_proxy,
#     "noProxy":None,
#     "proxyType":"MANUAL",
#     'autodetect':None
# }

# proxy = Proxy({
#     'proxyType': ProxyType.MANUAL,
#     'httpProxy': https_proxy ,
#     'ftpProxy': https_proxy,
#     'sslProxy': https_proxy  ,
#     'noProxy': '' # set this value as desired
#     })

# fake user agent
# profile.set_preference("general.useragent.override", useragent)
# profile.set_preference("network.proxy.type", 1)
# profile.set_preference("network.proxy.http", https_proxy)
# profile.set_preference("network.proxy.http_port", https_proxy_port)
# profile.set_preference("network.proxy.https", https_proxy)
# profile.set_preference("network.proxy.https_port", https_proxy_port)
# profile.update_preferences()
# dcap = dict(DesiredCapabilities.FIREFOX)
# dcap["firefox.page.settings.userAgent"] = (useragent)

#rotator

#no images
profile.set_preference('permissions.default.image', 2)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
#set fake UA
profile.set_preference("general.useragent.override", useragent)
options = Options()
options.headless = True
driver = Firefox(options=options, firefox_profile=profile)
timeout_int = 300
driver.set_page_load_timeout(timeout_int)


# rotate proxies technique should be applied to eliminate banning
#

# splits the string list of timestamps into tuple list ( day ,time )
#timestamps_list : list of timestamps in string format
def split_timestamps(timestamps_list):
    t = tuple()
    tp = list()
    for ts in timestamps_list:
        m: Optional[Match[str]] = re.match(r'(?P<day>^.*), (?P<timestamp>\d{2}:\d{2})', ts)
        if m:
            t = (m.group('day'), m.group('timestamp'))
#            print(t)
            tp.append(t)
    return tp

attempts_int = 10
attempts = 0
page_loaded = False
#for clean up actions the finalize block is set at the bottom of the code
try:
    #forcr page o load in case of proxy server slowdown
    while attempts < attempts_int and not page_loaded:
        try:
            driver.get(sortedItemsLocationLink)
        except WebDriverException as errw:
            print('Tried ', attempts, ' out of ', attempts_int)
            print("WebDriverException", errw)
            if 'Reached error page' in str(errw) :
                attempts = attempts + 1
            else:
                raise SystemExit(errw)
        except TimeoutException as errt:
            print('Tried ', attempts,' out of ',attempts_int)
            print("Timeout Error:", errt)
            timeout_int = 2 * timeout_int
            driver.set_page_load_timeout(timeout_int)
            attempts = attempts + 1
            print('Timeout doubled ',timeout_int)
        finally:
            page_state = driver.execute_script('return document.readyState;')
            if  page_state == 'complete' :
                page_loaded = True
    # reference to the date in html code
    timestampxpath = "//div[@data-marker='item/datetime']"
    # reference to the realty item that stands for flat
    appartmentxpath = "//a[contains(text(),'квартира')]"
    # neccessary delay to load up the page
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # scroll down the page till the yesterdays' mark is not present
    # to discover daily listing of ads

    # initialization
    # we feed in the cycle with the timestamps that have been already loaded
    timestamp = driver.find_elements_by_xpath(timestampxpath)
    ls = list(map(lambda x: x.text, timestamp))
    allday = False
    scrolldown = True
    # timestamp of the last item is set
    while not allday:
        t = split_timestamps(ls)
   #     print(t)
        #get day tags and make up  a set
        days = [*map(lambda x: x[0], t )]
        uniquedays = set( days  )
        #    m= re.match(r'(?P<day>^.*), (?P<timestamp>\d{2}:\d{2})', ls[-1])
        stoptag = 'Вчера'
        if stoptag in uniquedays:
            #freq = freq_consecutive_duplicates(days)
            #eliminate the ads
            #print([f[1] for f in  freq  if f[0] == stoptag])
            #if max([f[1] for f in  freq  if f[0] == stoptag]) >= 2:
            if days[-1] == stoptag and days[-2] == stoptag:
                # sample = open('freq.txt', 'w')
                # print (freq, file = sample)
                # sample.close()
                # quit once the mark found more than 30 times ie about the size of the screen
                allday = True
                scrolldown = False
        if scrolldown:
                # click a button to expand the list
                loadmorebuttonxpath = "//span[contains(text(),'Загрузить еще')]"
                attempts_int = 10
                attempts = 0
                page_loaded = False
                loadmorebutton = None
                while attempts < attempts_int and not page_loaded:
                    try:
                        loadmorebutton = driver.find_element_by_xpath(loadmorebuttonxpath)
                    except NoSuchElementException as errnoel:
                        print('Tried ', attempts, ' out of ', attempts_int)
                        print("No click more button error:", errnoel)
                        attempts = attempts + 1
                        print("Wait for more time..")
                        time.sleep(20)
                    finally:
                        page_state = driver.execute_script('return document.readyState;')
                        if page_state == 'complete':
                            page_loaded = True
                try:
                    loadmorebutton.click()
                except Exception as nobutton:
                    raise SystemExit(nobutton)
                time.sleep(1)
                timestamp = driver.find_elements_by_xpath(timestampxpath)
                print('links found:', len(timestamp))
                time.sleep(1)
                ls = list(map(lambda x: x.text, timestamp))

   # parse links that are present after scroll
    realtylinks = driver.find_elements_by_xpath(appartmentxpath)
    # print em out
    hrefs = list(map(lambda x: x.get_attribute('href'), realtylinks))
    print (*hrefs, sep='\n')
    # parse datastamps
    timestamp = driver.find_elements_by_xpath(timestampxpath)
    print( list(map(lambda x: x.text, timestamp)) )
    for i in range(0, len(hrefs) - 1):
        parse_realty_page( hrefs[i])
    #run_parallel_selenium_singlecore(realtylinks,parse_realty_page)
    #time.sleep(20)

# clean up the selenium driver resources in any case
# memory leak could occur once not completed gracefully

finally:
    tmp = scrshotpath  + tempfile.NamedTemporaryFile().name + ".png"
    print(tmp)
    driver.get_screenshot_as_file(tmp)
    driver.quit()


