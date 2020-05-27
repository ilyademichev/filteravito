import re
import time
from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
useragent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
            'Version/12.0 Mobile/15E148 Safari/604.1 '

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["firefox.page.settings.userAgent"] = (useragent)
httsps_proxy_domain = "93.159.236.30"
https_proxy_port = "8080"
#
profile = webdriver.FirefoxProfile()
#proxy server settings
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", httsps_proxy_domain)
profile.set_preference("network.proxy.http_port", https_proxy_port)
profile.set_preference("network.proxy.ssl", httsps_proxy_domain)
profile.set_preference("network.proxy.ssl_port", https_proxy_port)
#fake user agent
profile.set_preference("general.useragent.override", useragent)
options = Options()
options.headless = False

driver = Firefox(options=options,firefox_profile=profile  )

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
    m = re.search(r'(?P<day>^.*), (?P<timestamp>\d{2}:\d{2})', ts)
    if m :
        print( m.group('day'))
        print( m.group('timestamp'))
allday = False
#initialization
#timestamp of the last item is set
#scroll till the yesterday mark is not presend
#to discover all day listing of ads
while not allday :
    m = re.search(r'(?P<day>^.*), (?P<timestamp>\d{2}:\d{2})', ls[-1])
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