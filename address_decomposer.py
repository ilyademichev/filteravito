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


class AvitoAddressDecomposer(Thread):
    """ Splits the string address into fields """
    def __init__(self,dbm,regions=[],districts=[],localities=[],streets=[],houses=[]):
        if dbm is None:
            parser_logger.info("* Thread {0} - Database manager object is required".format(self.name))
            raise  ValueError
        self.__database_manager = dbm
        self.__queue = Queue()
        # dictionaries to search from
        self.regions = regions
        self.districts =districts
        self.localities=localities
        self.streets=streets
        self.houses=houses

    @property
    def regions(self):
        return self.__regions

    @regions.setter
    def regions(self, val):
        if val < 0:
            self.__regions = 0
        elif val > 1000:
            self.__regions = 1000
        else:
            self.__regions = val

    def run(self):
        """ decomposes the adress s and push the address object into database queue"""
        while True:
            # gets the adress item from the queue
            s = self.__queue.get(block=True,timeout=None)
            parser_logger.info("* Thread {0} - decomposing address".format(self.name))
            a = self.decompose( s )
            if a is None:
                parser_logger.error("* Thread {0} - address decomposing failed : {1} ".format(self.name, s))
            else:
                self.__database_manager.
            # send a signal to the queue that the job is done
            self.__queue.task_done()

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

class AddressManager:
    def __init__(self,download_manager, download_dict=None, thread_count=1):
        pass
    def begin_addr_sync(self):
        pass
    def queue_addresses(self, addresses_list):
        pass
    def endup_addr_sync(self):
        pass






