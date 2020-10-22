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

    def set_random_firefox_proxy(self):
        """
        sets random proxy from proxies list
        :return:
        True if profile file altered and saved
        False on IO errors of REGEX errors
        """
        profile = webdriver.FirefoxProfile(CrawlerData.FF_PROFILE_PATH)
        try:
            prof_file = open(CrawlerData.FF_PROFILE_PATH +  CrawlerData.FF_PROFILE_FILE  ,"r")
            p = self.proxies[random.randrange(0,len(self.proxies)-1)]
            proxy_ip, separator, proxy_port = p.rpartition(':')
            # replace proxy and port in profile settings
            # exert:
            # user_pref("network.proxy.ftp", "95.28.233.106");
            # user_pref("network.proxy.ftp_port", 8080);
            # user_pref("network.proxy.http", "95.28.233.106");
            # user_pref("network.proxy.http_port", 8080);
            # user_pref("network.proxy.share_proxy_settings", true);
            # user_pref("network.proxy.ssl", "95.28.233.106");
            # user_pref("network.proxy.ssl_port", 8080);
            # user_pref("network.proxy.type", 1);
            fileContents = prof_file.read()

            pat_ftp = r"\"network\.proxy\.ftp\", \"(?P<proxy_FTP>)\""
            pat_http = r"\"network\.proxy\.http\", \"(?P<proxy_HTTP>)\""
            pat_ssl = r"\"network\.proxy\.ssl\", \"(?P<proxy_SSL>)\""
            pat_ip = re.compile(pat_ftp + "|" + pat_http + "|" + pat_ssl)
            fileContents = pat_ip.sub(proxy_ip, r"\g<proxy_FTP> \g<proxy_HTTP> \\g<proxy_SSL>", fileContents)

            pat_ftp_port = re.compile(r"\"network\.proxy\.ftp_port\", (?P<port_FTP>\d{1,5})")
            pat_http_port = re.compile(r"\"network\.proxy\.http_port\", (?P<port_HTTP>\d{1,5})")
            pat_ssl_port = re.compile(r"\"network\.proxy\.ssl_port\", (?P<port_SSL>\d{1,5})")
            #compile regexp into single regexp wit hreplcaement

            pat_port = re.compile(pat_ftp_port + "|" + pat_http_port + "|" + pat_ssl_port)
            fileContents = pat_port.sub(proxy_port, r"\g<port_FTP> \g<port_HTTP> \\g<port_SSL>", fileContents)

            prof_file.seek(0)
            prof_file.truncate()
            prof_file.write(fileContents)
            # images_div = self.driver.find_elements(*Locators.IMAGES_CONTAINER_SCRIPT)
            # res = pat.findall(images_div[0].get_attribute('innerHTML'))
            return True
        except OSError as e:
            parser_logger.error("Firefox profile file IO error: ", exc_info=True)
            return False
        except  IndexError as e:
            parser_logger.error("Group pattern in regexp error ", exc_info=True)
            return False




