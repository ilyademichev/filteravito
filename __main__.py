import time

from avito_parser import AvitoParser
from crawler_data import CrawlerData

algorithm = {
    #"TASK 0": ["Боровск"]
    "Все окрестности": ["Жуков","Малоярославец","Наро-Фоминск","Обнинск","Боровск"]
    #"Массовый":["Москва"]
    #"TASK 2": ["Обнинск", "Обнинск", "Обнинск"]  # ,
    # "TASK 3":["Москва", "Обнинск", "Москва", "Обнинск","Москва", "Обнинск"]
}
if __name__ == "__main__":

    for i in range(0,100):
        try:

            p = AvitoParser()
            p.run_parser_task(algorithm)
            # introduce some delay between parser reruns to free up the resources
            time.sleep(CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS)


        except Exception as e:
            parser_logger.error("Error on algorithm execution", exc_info=True)


