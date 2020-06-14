profile = webdriver.FirefoxProfile('/home/user/.mozilla/firefox/n34w7dcm.user/')
profile.set_preference("general.useragent.override","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0")
profile.set_preference("places.history.enabled", False)
profile.set_preference("privacy.clearOnShutdown.offlineApps", True)
profile.set_preference("privacy.clearOnShutdown.passwords", True)
profile.set_preference("privacy.clearOnShutdown.siteSettings", True)
profile.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
profile.update_preferences()


change fonts, resolution, user agents, webgl

Try to use selenium with a specific user profile of chrome, That way you can use it as specific user and define any thing you want, When doing so it will run as a 'real' user, look at chrome process with some process explorer and you'll see the difference with the tags.

For example:

username = os.getenv("USERNAME")
userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir={}".format(userProfile))
# add here any tag you want.
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])
chromedriver = "C:\Python27\chromedriver\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)





I've found changing the javascript "key" variable like this:

//Fools the website into believing a human is navigating it
        ((JavascriptExecutor)driver).executeScript("window.key = \"blahblah\";");

works for some websites when using Selenium Webdriver along with Google Chrome, since many sites check for this variable in order to avoid being scrapped by Selenium.
