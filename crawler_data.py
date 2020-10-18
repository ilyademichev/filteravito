class CrawlerData:
    MSACCESS_DB_PATH_WINDOWS = "C:\\REALTYDB\\"
    MSACCESS_DB_FILENAME_WINDOWS = r"realty - Copy.accdb"
    MSACCESS_IMPORT_IMAGES_MACRO = r'AddImageAttchmMacro'
    IMAGE_FOLDER =r"avito_images_by_adv_id"
    FF_EXECUTABLE_PATH=""
    BASE_URL = r"https://www.m.avito.ru"
    FF_PROFILE_PATH = \
        r"C:\Users\ilyademichev\AppData\Roaming\Mozilla\Firefox\Profiles\b9jixrd6.avitoproxy"
    SORTED_ITEMS_LOCATION_LINK = r"https://m.avito.ru/LOCATION/kvartiry?s=104"
    LOCATION_TAG = r"LOCATION"
    YESTERDAY_TAG = r"Вчера"
    TODAY_TAG = r"Сегодня"
    #http download selenim driver timeout
    IMPLICIT_TIMEOUT_INT_SECONDS = 180
    #image downloader timeout
    IMPLICIT_CDN_TIMEOUT_INT_SECONDS = 120
    SCR_SHOT_PATH = r'scrshotavito/'
    ATTEMPTS_INT = 30 # maximum one hour wait
    SCROLL_PAUSE_TIME = 15


