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
https_proxy_domain = "93.159.236.30"
https_proxy_port = "8080"
https_proxy = https_proxy_domain + ":" + https_proxy_port
profile = webdriver.FirefoxProfile("/home/ilya/.mozilla/firefox/vfwzppqq.avitoproxy")


#proxy server settings

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

#fake user agent
# profile.set_preference("general.useragent.override", useragent)
# profile.set_preference("network.proxy.type", 1)
# profile.set_preference("network.proxy.http", https_proxy)
# profile.set_preference("network.proxy.http_port", https_proxy_port)
# profile.set_preference("network.proxy.https", https_proxy)
# profile.set_preference("network.proxy.https_port", https_proxy_port)
# profile.update_preferences()
# dcap = dict(DesiredCapabilities.FIREFOX)
# dcap["firefox.page.settings.userAgent"] = (useragent)

profile.set_preference("general.useragent.override",useragent )
options = Options()
options.headless = False
driver = Firefox(options = options,firefox_profile = profile  )

driver.get('https://m.avito.ru/obninsk/nedvizhimost?sort=date')
#reference to the date in html code
timestampxpath = "//div[@data-marker='item/datetime']"
#reference to the realty item that stands for flat
appartmentxpath = "//a[contains(text(),'квартира')]"
#neccessary delay to load up the page
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
#parse links that are preenst after scroll
time.sleep(20)
realtylinks = driver.find_elements_by_xpath(appartmentxpath)
time.sleep(20)
#print em out
print(*( map(lambda x: x.get_attribute('href'), realtylinks ) ), sep='\n')
time.sleep(20)
#parse datastamps
timestamp = driver.find_elements_by_xpath(timestampxpath)
time.sleep(20)
ls = list(map(lambda x: x.text, timestamp ))
#print them
print( ls)
#split date into day an time
for ts in ls:
    m: Optional[Match[str]] = re.search(r'(?P<day>^.*), (?P<timestamp>\d{2}:\d{2})', ts)
    if m :
        print( m.group('day'))
        print( m.group('timestamp'))
allday = False
#initialization
#timestamp of the last item is set
#scroll till the yesterday mark is not presend
#to discover all day listing of ads
while not allday :

    m= re.search(r'(?P<day>^.*), (?P<timestamp>\d{2}:\d{2})', ls[-1])
    if m :
        #quit once the mark found
        if m.group('day') == 'Вчера' :
            allday = True
        else:
            #click a button to expand the list
            loadmorebuttonxpath = "//span[contains(text(),'Загрузить еще')]"
            loadmorebutton = driver.find_element_by_xpath(loadmorebuttonxpath)
            time.sleep(3)
            loadmorebutton.click()
            time.sleep(3)

            timestamp = driver.find_elements_by_xpath(timestampxpath)
            time.sleep(10)
            ls = list(map(lambda x: x.text, timestamp))


driver.quit()