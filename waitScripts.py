from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def waitForJSandJQueryToLoad(driver) :

    WebDriverWait wait =  WebDriverWait(driver, 30);

    // wait for jQuery to load
    EC. jQueryLoad =  EC.<Boolean>() {
      @Override
      public Boolean apply(WebDriver driver) {
        try {
          return ((Long)((JavascriptExecutor)getDriver()).executeScript("return jQuery.active") == 0);
        }
        catch (Exception e) {
          // no jQuery present
          return true;
        }
      }
    };

    // wait for Javascript to load
    ExpectedCondition<Boolean> jsLoad = new ExpectedCondition<Boolean>() {
      @Override
      public Boolean apply(WebDriver driver) {
        return ((JavascriptExecutor)getDriver()).executeScript("return document.readyState")
        .toString().equals("complete");
      }
    };

  return wait.until(jQueryLoad) && wait.until(jsLoad);
}

