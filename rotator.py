srchidemy = 'http://free-proxy.cz/en/proxylist/country/RU/https/ping/all'
proxyList  = list()
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': useragent,
    }
)

try:
    page = requests.get(srchidemy,headers=headers)
    page.raise_for_status()
    print(page.content)
    tree = html.fromstring(page.content)
    proxyList.append(tuple(zip(tree.xpath('//tbody/tr[1]/td[1]'), tree.xpath('//tbody/tr[1]/td[2]'))))
except requests.exceptions.HTTPError as errh:
    print("Http Error:", errh)
except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
except requests.exceptions.RequestException as err:
    raise SystemExit(e)