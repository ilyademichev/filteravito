from parser_logger import parser_logger
from avito_parser import AvitoParser
from database_manager import DatabaseManager
from image_download_manager import DownloadManager

algorithm = {
    # "TASK 0": ["Боровск"]
    "Все окрестности Обнинск": ["Жуков","Малоярославец","Наро-Фоминск","Обнинск","Боровск"]
    # "Подмосковье": ["Подольск", "Химки"]
    # "Массовый Центр": ["Москва"],
    # "Массовый Юг": ["Краснодар"]
    # "TASK 2": ["Обнинск", "Обнинск", "Обнинск"]  # ,
    # "TASK 3":["Москва", "Обнинск", "Москва", "Обнинск","Москва", "Обнинск"]
}
dwm = None
dbm = None
# singleton class for ORM operations
dbm = DatabaseManager ( dwm, thread_count=1 )
dwm = DownloadManager ( thread_count=4 )
dwm.database_manager = dbm
dbm.download_manager = dwm
for i in range ( 0, 1000 ) :
    try:
        # OOP agregation:
        # Parser uses DownloadManager
        # Parser uses DatabaseManager
        # DownloadManager uses DatabaseManager
        # DatabaseManager uses DownloadManager
        p = AvitoParser()
        # pc = CianParser()
        # pd = DomClickParser()
        parser_logger.info("Run {0}".format(str(i)))
        p.run_parser_task(algorithm, dwm, dbm)
    except Exception as e:
        parser_logger.error("Error on algorithm execution: ", exc_info=True)
    finally:
        # wait for CRUD queue
        if dbm is not None:
            dbm.endup_db_sync()
        # wait for images queue
        if dwm is not None:
            dwm.endup_downloads()
        if dbm is not None:
            # load attachments: images into db
            dbm.MSA_image_sync()
