import tempfile
import re
import time
from typing import Optional, Match

from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

useragent = 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H) AppleWebKit/534.30 (KHTML, ' \
            'like Gecko) Version/4.0 Mobile Safari/534.30 '

# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["firefox.page.settings.userAgent"] = (useragent)
scrshotpath = '/home/ilya/scrshotavito'
https_proxy_domain = "93.159.236.30"
https_proxy_port = "8080"
https_proxy = https_proxy_domain + ":" + https_proxy_port
profile = webdriver.FirefoxProfile("/home/ilya/.mozilla/firefox/vfwzppqq.avitoproxy")#asdf
#locations
#https://www.avito.ru/maloyaroslavets/nedvizhimost?s=104
#https://www.avito.ru/obninsk/nedvizhimost?s=104
sortedItemsLocationLink = 'https://m.avito.ru/maloyaroslavets/nedvizhimost?s=104'
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

profile.set_preference("general.useragent.override", useragent)
options = Options()
options.headless = True
driver = Firefox(options=options, firefox_profile=profile)
driver.set_page_load_timeout(240)


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
            print(t)
            tp.append(t)
    return tp


try:
    driver.get(sortedItemsLocationLink)
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
    # parse links that are present after scroll
    time.sleep(20)
    realtylinks = driver.find_elements_by_xpath(appartmentxpath)
    time.sleep(20)
    # print em out
    print(*(map(lambda x: x.get_attribute('href'), realtylinks)), sep='\n')
    time.sleep(20)
    # parse datastamps
    timestamp = driver.find_elements_by_xpath(timestampxpath)
    time.sleep(20)
    ls = list(map(lambda x: x.text, timestamp))
    # print them
    print(ls)
    # split date into day an time
    allday = False
    # initialization
    # timestamp of the last item is set
    # scroll till the yesterday mark is not presend
    # to discover all day listing of ads
    while not allday:
        t = split_timestamps(ls)
        print(t)
        #get day tags and make up  a set
        s = set(  map(lambda x: x[0], t ) )
        #    m= re.match(r'(?P<day>^.*), (?P<timestamp>\d{2}:\d{2})', ls[-1])
        if 'Вчера' in s:
            # quit once the mark found
            allday = True
        else:
                # click a button to expand the list
                loadmorebuttonxpath = "//span[contains(text(),'Загрузить еще')]"
                loadmorebutton = driver.find_element_by_xpath(loadmorebuttonxpath)
                time.sleep(3)
                loadmorebutton.click()
                time.sleep(3)
                timestamp = driver.find_elements_by_xpath(timestampxpath)
                time.sleep(10)
                ls = list(map(lambda x: x.text, timestamp))

# clean up the selenium driver resources in any case
# memory leak could occur once not completed gracefully

finally:
    tmp = scrshotpath  + tempfile.NamedTemporaryFile().name + ".png"
    print(tmp)
    driver.get_screenshot_as_file(tmp)
    driver.quit()
