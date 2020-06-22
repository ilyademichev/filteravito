 from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"return window.jQuery != undefined && jQuery.active==0"
class waitForJSandJQueryToLoad(object):
    def __init__(self, element):
        self.element = element

    def __call__(self, driver):
        WebDriverWait(ff_driver, 10).until(
            ajax_complete, "Timeout waiting for page to load")

def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except WebDriverException:
        pass



def waitForJSandJQueryToLoad
     ad(driver) :
    # wait for jQuery to load
    WebDriverWait wait = WebDriverWait(driver,30)
    EC.jQueryLoad =
        try :
            return driver.executeScript("return jQuery.active") == 0
        except Exception as e:
          # no jQuery present
            return True
    # wait for Javascript to load
    EC.jsLoad =
        return driver.executeScript("return document.readyState") == "complete"
    return wait.until(jQueryLoad) and wait.until(jsLoad)


