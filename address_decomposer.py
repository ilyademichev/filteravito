import re
from queue import Queue
from threading import Thread

from parser_logger import parser_logger


class Address:
    def __init__(self, s):
        self.full_address = s
        self.region = None
        self.regional_district = None
        self.locality = None
        self.street = None
        self.house = None
        self.empty_field = "-"
        self.street_prefix =("ул.","пр.","пр-т")

#
class AvitoAddressDecomposer(Thread):
    """"""
    def __init__(self):
        self.regions=[]
        self.districts=[]
        self.localities=[]
        self.streets=[]
        self.houses=[]
        self.queue = Queue()

    def run(self):
        while True:
            # gets the realty item from the queue
            (s,adv_number) = self.queue.get(block=True,timeout=None)
            parser_logger.info("* Thread {0} - decomposing address".format(self.name))
            a = self.decompose( s )
            if a is None:
                parser_logger.error("* Thread {0} - decomposing failed ".format(self.name))
            # send a signal to the queue that the job is done
            self.queue.task_done()

    def decompose(self, s):
        a = Address(s)
        #, пр-т Ленина, 3
        #, Ленинградская ул., 3к4
        #, ул. Объездная Дорога, 4 корпус 6 строение 7
        # or it could start without comma
        if any ( x in s for x in a.street_prefix ) :
            street_pattern = r"(, ([^,]+) (ул\.,|пр-т|пр\.))|(, (ул\.|пр-т|пр\.) ([^,]+),)"
            house_pattern = r"\d([^,]+)$| \d{1,2}$"
            locality_pattern=r""
            regional_district_pattern=r""
            region_pattern=r""
            if  re.search ( street_pattern, s, re.IGNORECASE ):
                # found_street = some group
                found_street = None
                if found_street in self.streets:
                    pass
                    # just write the steet code
                else:
                    pass
                    # add new street
                if re.search(house_pattern,s):
                    # found_house = some group
                    found_house = None
                    if found_house in self.houses:
                        pass
                        # just write the house code
                    else:
                        pass
                        # write new house and the code
                else:
                    a.house = a.empty_field
            else :
                a.street =a.empty_field

            if re.search(locality_pattern,s,re.IGNORECASE):
                pass
            else:
                a.locality = a.empty_field

            if re.search(regional_district_pattern,s,re.IGNORECASE):
                pass
            else:
                a.regional_district = a.empty_field

            if re.search(region_pattern,s,re.IGNORECASE):
                pass
            else:
                a.region = a.empty_field

            return a
        # no street found
        else:
            return None


