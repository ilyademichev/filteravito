class CrawlerData:
    MSACCESS_DB_PATH_WINDOWS = 'C:\\REALTYDB\\'
    MSACCESS_DB_FILENAME_WINDOWS = r"realty - Copy (2).accdb"
    MSACCESS_IMPORT_IMAGES_MACRO = r'AddImageAttchmMacro'
    IMAGE_FOLDER = 'avito_images_by_adv_id\\'
    FF_EXECUTABLE_PATH = ""
    BASE_URL = r"https://www.m.avito.ru"
    FF_PROFILE_PATH = \
        r"C:\Users\ilyademichev\AppData\Roaming\Mozilla\Firefox\Profiles\b9jixrd6.avitoproxy\\"
    FF_PROFILE_FILE = r"prefs.js"
    SORTED_APPARTMENTS_LOCATION_LINK = r"https://m.avito.ru/LOCATION/kvartiry?s=104"
    SORTED_ROOMS_LOCATION_LINK = r"https://m.avito.ru/LOCATION/komnaty?s=104"
    LOCATION_TAG = r"LOCATION"
    YESTERDAY_TAG = r"Вчера"
    PROXY_FILE = "proxy_list"
    TODAY_TAG = r"Сегодня"
    # http download selenim driver timeout
    IMPLICIT_TIMEOUT_INT_SECONDS = 300
    # image downloader timeout
    IMPLICIT_CDN_TIMEOUT_INT_SECONDS = 120
    SCR_SHOT_PATH = r'scrshotavito/'
    ATTEMPTS_INT = 30  # maximum one hour wait
    SCROLL_PAUSE_TIME = 40
