import ipaddress
import logging

from selenium.webdriver.firefox import webdriver

from crawler_data import CrawlerData


class ProxyServerManager():
    """
    reads proxy file list and validates the IP format
    """
    proxies = []
    firefox_profile_path = None
    def __init__(self, proxy_list_file,ff_prfofile_path):
        if  ff_prfofile_path or  ff_prfofile_path is None:
            raise ValueError
        try:
            p_file = open(proxy_list_file, "r")
            proxies = p_file.readlines()
            for p in proxies:
                ipaddress.IPv4Address(p)
        except OSError as e:
            logging.error("File of proxies IO error: ", exc_info=True)
        except ValueError as e:
            logging.error("Wrong IP in proxy file: ", exc_info=True)

    def set_firefox_proxy(self):
        """
        sets random proxy from proxies list
        :return:
        """
        profile = webdriver.FirefoxProfile(CrawlerData.FF_PROFILE_PATH)
        try:
            prof_file = open(CrawlerData.FF_PROFILE_PATH,"r")
            

        except OSError as e:
            logging.error("Firefox profile file IO error: ", exc_info=True)



