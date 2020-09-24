import logging
import time

from sqlalchemy.orm import create_session, relationship,sessionmaker
from sqlalchemy.sql import exists
from avito_parser import AvitoParser
from crawler_data import CrawlerData
from realty_appartment_page import RealtyApartmentPage
from realty_db import RealtyItem, Company, Rooms, RealtyStatus, AdvertismentSource

algorithm = {
    #"TASK 0": ["Боровск"]
    #"Все окрестности": ["Жуков","Малоярославец","Наро-Фоминск","Обнинск","Боровск"]
    "Массовый":["Москва"]
    #"TASK 2": ["Обнинск", "Обнинск", "Обнинск"]  # ,
    # "TASK 3":["Москва", "Обнинск", "Москва", "Обнинск","Москва", "Обнинск"]
}
for i in range(0,100):
    try:
        p = AvitoParser()
        p.run_parser_task(algorithm)
        # introduce some delay between parser reruns to free up the resources
        time.sleep(CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS)
    except Exception as e:
        logging.error("Error on algorithm execution", exc_info=True)
    finally:
        p.dispose()







