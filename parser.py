# parse links that are present after scroll
# returns the list of links
def parse_realtylinks(driver):
        realtylinks = driver.find_elements_by_xpath(appartmentxpath)
        # trace print em out
        #print(*(map(lambda x: x.get_attribute('href'), realtylinks)), sep='\n')
        return *(map(lambda x: x.get_attribute('href'), realtylinks))


#frequencies of consequetive  occurencies in a list
def freq_consecutive_duplicates(ls_str):
    return [(key, sum(1 for i in group)) for key, group in groupby(ls_str)]

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
#simulate user scroll untill the load more button is unveiled
def scroll_down_till_button_present(driver):
        #scroll down
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
#click the load more button till the server sends data
#the output limit measured
#Moscow 3320 references to appartments
#St Petersburg
#once the load more button is not present quit
def scroll_down_with_button_click(driver,attempts_int = 3):
    YESTERDAYTAG = 'Вчера'
    LOAD_MORE_BUTTON_XPATH = "//span[contains(text(),'Загрузить еще')]"
    # initialization
    # we feed in the cycle with the timestamps that have been already loaded
    timestamp = driver.find_elements_by_xpath(timestampxpath)
    ls = list(map(lambda x: x.text, timestamp))
    allday = False #flags that the daily output has completed
    scrolldown = True #flags for more scroll down needed
    # timestamp of the last item is set
    while not allday:
        t = split_timestamps(ls)
        #     print(t)
        # get day tags and make up  a set
        days = [*map(lambda x: x[0], t)]
        uniquedays = set(days)
        #    m= re.match(r'(?P<day>^.*), (?P<timestamp>\d{2}:\d{2})', ls[-1])
        if YESTERDAYTAG in uniquedays:
            # The break criteria
            # Once we meet more than 2 sequential occurences of YESTERDAYTAG  we break the cycle
            # The  output is mixed with ads that can be of any date.
            # But never ads come in sequential order they appear randomly;
            # So once YESTERDAYTAG is met more than twice sequentally
            # we found the real YESTERDAY's item not the advertisment
            freq = freq_consecutive_duplicates(days)
            if max([f[1] for f in freq if f[0] == YESTERDAYTAG]) >= 2:
                # sample = open('freq.txt', 'w')
                # print (freq, file = sample)
                # sample.close()
                # quit once the mark found more than 30 times ie about the size of the screen
                allday = True
                scrolldown = False
        if scrolldown:
            # click a button to expand the list
            attempts = 0
            page_loaded = False
            loadmorebutton = None
            while attempts < attempts_int and not page_loaded:
                try:
                    loadmorebutton = driver.find_element_by_xpath(LOAD_MORE_BUTTON_XPATH)
                except NoSuchElementException as errnoel:
                    print('Tried ', attempts, ' out of ', attempts_int)
                    print("No click more button error:", errnoel)
                    attempts = attempts + 1
                    print("Wait for more time..")
                    time.sleep(10)
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
            print('links found:', timestamp.len())
            time.sleep(1)
            ls = list(map(lambda x: x.text, timestamp))


def parse_realtylinks_from_filter_page(driver,location,tries=3) :
    # substitute the nesessary location instead of LOCATION
    TEMPLATE_LOCATION_LINK = 'https: // m.avito.ru / LOCATION / nedvizhimost?s = 104'
    # reference to the date in html code
    timestampxpath = "//div[@data-marker='item/datetime']"
    # reference to the realty item that stands for flat
    appartmentxpath = "//a[contains(text(),'квартира')]"
    # neccessary delay to load up the page whilst scrolling down
    SCROLL_PAUSE_TIME = 0.5
    sortedItemsLocationLink = TEMPLATE_LOCATION_LINK.replace('LOCATION',location)
    attempts_int = tries
    attempts = 0
    # flag for jquery processed and html loaded
    page_loaded = False

    #for clean up actions the finalize block is  at the bottom of the code
    try:
        #
        #force page to load attempts_int times in case of proxy server slowdown
        #scroll down to open up all content
        #
        while attempts < attempts_int and not page_loaded:
            try:
                driver.get(sortedItemsLocationLink)
            #proxy overload
            #launch a retry
            except WebDriverException as errw:
                print('Tried ', attempts, ' out of ', attempts_int)
                print("WebDriverException", errw)
                if 'Reached error page ' in str(errw) :
                    attempts = attempts + 1
                else:
                    raise SystemExit(errw)
            #slow network detected
            #launch a retry
            #double the wait time for the driver
            except TimeoutException as errt:
                print('Tried ', attempts,' out of ',attempts_int)
                print("Timeout Error:", errt)
                timeout_int = 2 * timeout_int
                driver.set_page_load_timeout(timeout_int)
                attempts = attempts + 1
                print('Timeout doubled ',timeout_int)
            #check if jquery processed and html loaded
            finally:
                page_state = driver.execute_script('return document.readyState;')
                if  page_state == 'complete' :
                    page_loaded = True
        # scroll down the page till the yesterdays' mark is not present
        # to discover daily listing of ads
        scroll_down_till_button_present(driver)
        scroll_down_with_button_click(driver)
    # clean up the selenium driver resources in any case
    # memory leak could occur once not completed gracefully

    finally:
        tmp = scrshotpath  + tempfile.NamedTemporaryFile().name + ".png"
        print(tmp)
        driver.get_screenshot_as_file(tmp)
        driver.quit()
