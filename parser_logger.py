import logging
import os
import random
import datetime
# parser logging  settings
import uuid

from crawler_data import CrawlerData

now = datetime.datetime.now()
logname = str(now.strftime('%Y-%m-%dT%H-%M-%S')) + " parser.log"
tmp_folder = str(uuid.uuid4()) + "/"
CrawlerData.SCR_SHOT_PATH += tmp_folder
os.mkdir(CrawlerData.SCR_SHOT_PATH)
# logging.basicConfig(handlers=[logging.FileHandler(filename=logname,encoding='utf-8', mode='a+')],
#                     level=logging.DEBUG,
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S')
parser_logger= logging.getLogger()
parser_logger.setLevel(logging.INFO)
handler = logging.FileHandler(logname, 'w', 'utf-8')
formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s','%H:%M:%S')
handler.setFormatter(formatter)
parser_logger.addHandler(handler)
# make separate folder for images

