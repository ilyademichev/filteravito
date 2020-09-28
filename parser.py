import logging
from avito_parser import AvitoParser
from database_manager import DatabaseManager
from image_download_manager import DownloadManager
algorithm = {
    #"TASK 0": ["Боровск"]
    #"Все окрестности": ["Жуков","Малоярославец","Наро-Фоминск","Обнинск","Боровск"]
    "Массовый":["Москва"]
    #"TASK 2": ["Обнинск", "Обнинск", "Обнинск"]  # ,
    # "TASK 3":["Москва", "Обнинск", "Москва", "Обнинск","Москва", "Обнинск"]
}
try:
        #OOP agregation:
        #Parser uses DownloadManager
        #Parser uses DatabaseManager
        #DownloadManager uses DatabaseManager
        #DatabaseManager uses DownloadManager
        p = AvitoParser()
        #pc = CianParser()
        #pd = DomClickParser()
        dwm = DownloadManager(thread_count=4)
        dbm = DatabaseManager(thread_count=1)
        dwm.database_manager = dbm
        dbm.download_manager = dwm
        p.run_parser_task(algorithm,dwm , dbm)
except Exception as e:
        logging.error("Error on algorithm execution: ", exc_info=True)
finally:
        #wait for CRUD queue
        dbm.endup_db_sync()
        #wait for images queue
        dwm.endup_downloads()
        #load attachments into db
        dbm.MSA_image_sync()










