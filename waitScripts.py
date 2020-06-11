 from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class waitForJSandJQueryToLoad(object):
    def __init__(self, element):
        self.element = element

    def __call__(self, driver):

def waitForJSandJQueryToLoad(driver) :
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


