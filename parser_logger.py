import logging
import random
import datetime
# parser logging  settings
now = datetime.datetime.now()
logname = str(now.strftime('%Y-%m-%dT%H-%M-%S')) + " parser.log"
# logging.basicConfig(handlers=[logging.FileHandler(filename=logname,encoding='utf-8', mode='a+')],
#                     level=logging.DEBUG,
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S')
parser_logger= logging.getLogger()
parser_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(logname, 'w', 'utf-8')
formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s','%H:%M:%S')
handler.setFormatter(formatter)
parser_logger.addHandler(handler)