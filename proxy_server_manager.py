import ipaddress
import parser_logger
import random
import re

import pat as pat
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
            parser_logger.error("File of proxies IO error: ", exc_info=True)
        except ValueError as e:
            parser_logger.error("Wrong IP in proxy file: ", exc_info=True)

    def set_firefox_proxy(self):
        """
        sets random proxy from proxies list
        :return:
        """
        profile = webdriver.FirefoxProfile(CrawlerData.FF_PROFILE_PATH)
        try:
            prof_file = open(CrawlerData.FF_PROFILE_PATH +  CrawlerData.FF_PROFILE_FILE  ,"r")
            p = self.proxies[random.randrange(0,len(self.proxies)-1)]
            proxy = p
            port = p
            # replace proxy
            # user_pref("network.proxy.ftp", "95.28.233.106");
            # user_pref("network.proxy.ftp_port", 8080);
            # user_pref("network.proxy.http", "95.28.233.106");
            # user_pref("network.proxy.http_port", 8080);
            # user_pref("network.proxy.share_proxy_settings", true);
            # user_pref("network.proxy.ssl", "95.28.233.106");
            # user_pref("network.proxy.ssl_port", 8080);
            # user_pref("network.proxy.type", 1);
            pat_ftp = re.compile(r"\"network\.proxy\.ftp\", ")
            pat_http = re.compile(r"\"network\.proxy\.http\", ")
            pat_ssl = re.compile(r"\"network\.proxy\.ssl\", ")
            pat_ftp_port = re.compile(r"\"network\.proxy\.ftp_port\", ")
            pat_http_port = re.compile(r"\"network\.proxy\.http_port\", ")
            pat_ssl_port = re.compile(r"\"network\.proxy\.ssl_port\", ")
            #compile regexp into single regexp wit hreplcaement

            fileContents = prof_file.read()
            textPattern = re.compile(re.escape(text), flags)
            fileContents = textPattern.sub(subs, fileContents)

            file.seek(0)
            file.truncate()
            file.write(fileContents)
            # images_div = self.driver.find_elements(*Locators.IMAGES_CONTAINER_SCRIPT)
            # res = pat.findall(images_div[0].get_attribute('innerHTML'))
            if not pat is None:
                res = pat.findall(prof_file)
                # making up a proper link
                self.realty_images = ["http://" + re.sub(r"\%2F", "/", w) for w in res]
                parser_logger.info("Item page parsing: (Image urls 640x480): {0}".format(res))
                return True
            else:
                return False

        except OSError as e:
            parser_logger.error("Firefox profile file IO error: ", exc_info=True)



