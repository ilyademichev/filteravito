from enum import Enum
import requests
from lxml import html


class serverProtocol(Enum):
    HTTPS = 'https'
    HTTP = 'http'
    SOCKS5 = 'socks5'



def scrapProxies:
    srchidemy = 'https://hidemy.name/en/proxy-list/?country=RU&type=s#list'
    srcspysone = 'spys.one/proxys/RU/'
    srcfreeproxycz ='http://free-proxy.cz/en/proxylist/country/RU/https/ping/all'


class proxyScrapper(object):
    proxylistlink : str
    proxyList : list()
    # Constructor
    def __init__(self, proxylistlink):
        self.proxylistlink = proxylistlink
        # To get name

    def getProxylistlink(self):
        return self.proxylistlink

        # To check if this person is employee

    def scrapProxies(self,proxyProtocol):

    def collectLists(self):

        def inheritors(klass):
            subclasses = set()
            work = [klass]
            while work:
                parent = work.pop()
                for child in parent.__subclasses__():
                    if child not in subclasses:
                        subclasses.add(child)
                        work.append(child)
            return subclasses
        children = inheritors(self)
        for c in children:
            self.proxyList.append(c.proxyList)

class hidemyScrapper(proxyScrapper):
    def __init__(self):
        super( srchidemy )
    def scrapProxies(self):
        try:
            page = requests.get(self.proxylistlink)
            page.raise_for_status()
            tree = html.fromstring(page.content)
            self.proxyList.append( tuple( zip(tree.xpath('//tbody/tr[1]/td[1]'),tree.xpath('//tbody/tr[1]/td[2]') ))
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            raise SystemExit(e)

class freeproxyczScraper(proxyScrapper):
    def __init__(self):
        super( srchidemy )
    def scrapProxies(self):
        try:
            page = requests.get(self.proxylistlink)
            page.raise_for_status()
            tree = html.fromstring(page.content)
            #/ html / body / table[2] / tbody / tr[4] / td / table / tbody / tr[4] / td[1] / font
            self.proxyList.append( tuple( zip(tree.xpath('//tbody/tr[1]/td[1]'),tree.xpath('//tbody/tr[1]/td[2]') ))
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            raise SystemExit(e)
