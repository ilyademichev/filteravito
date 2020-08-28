import logging

import win32api,time
from win32com.client import Dispatch

from crawler_data import CrawlerData
try:
    strDbName = CrawlerData.MSACCESS_DB_PATH_WINDOWS + \
        CrawlerData.MSACCESS_DB_FILENAME_WINDOWS
    objAccess = Dispatch("Access.Application")
    objAccess.Visible = True
    objAccess.OpenCurrentDatabase(strDbName)
    objDB = objAccess.CurrentDb()
    objAccess.DoCmd.RunMacro(CrawlerData.MSACCESS_IMPORT_IMAGES_MACRO)
except Exception as e:
    logging.error("COM ERROR", exc_info=True)
finally:
    objAccess.Application.Quit()