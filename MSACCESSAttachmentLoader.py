import parser_logger

import win32api,time
from win32com.client import Dispatch
from crawler_data import CrawlerData

class MSA_attachment_loader:
    def __init__(self):
        try:
            strDbName = CrawlerData.MSACCESS_DB_PATH_WINDOWS + \
                        CrawlerData.MSACCESS_DB_FILENAME_WINDOWS
            self.objAccess = Dispatch("Access.Application")
            self.objAccess.Visible = False
            self.objAccess.OpenCurrentDatabase(strDbName)
            objDB = self.objAccess.CurrentDb()
        except Exception as e:
            parser_logger.error("MSA COM ERROR ", exc_info=True)
            self.objAccess.Application.Quit()

    #CrawlerData.MSACCESS_IMPORT_IMAGES_MACRO
    def launch_macro(self,macro_name):
        try:
            self.objAccess.DoCmd.RunMacro(macro_name)
        except Exception as e:
            parser_logger.error("MSA COM ERROR ", exc_info=True)

    def dispose(self):
        self.objAccess.Application.Quit()