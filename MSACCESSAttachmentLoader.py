from parser_logger import parser_logger
from win32com.client import Dispatch
from crawler_data import CrawlerData


class MSAttachmentLoader :
    def __init__(self) :
        strDbName = CrawlerData.MSACCESS_DB_PATH_WINDOWS + \
                    CrawlerData.MSACCESS_DB_FILENAME_WINDOWS
        self.objAccess = Dispatch ( "Access.Application" )
        # self.objAccess.Visible = True
        self.objAccess.Visible = False
        self.objAccess.OpenCurrentDatabase ( strDbName )
        # self.objDB = self.objAccess.CurrentDb()

    # CrawlerData.MSACCESS_IMPORT_IMAGES_MACRO
    def launch_macro(self, macro_name) :
        self.objAccess.DoCmd.RunMacro ( macro_name )

    def dispose(self) :
        #        pass
        self.objAccess.DoCmd.CloseDatabase ()
        self.objAccess.Application.Quit ()
        # del self.objAccess
