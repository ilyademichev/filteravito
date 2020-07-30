""" Import """
# https://pastebin.com/QrZG9e9T
import logging
import os
import time
from threading import Thread
from queue import Queue
import argparse
import binascii
import urllib.request
import requests
from crawler_data import CrawlerData

#queue item is a tuple
# ("advertisment number":[Link 1,Link 2,Link3,...])
class Downloader(Thread):
    """ Downloader class - reads queue and downloads each file in succession """
    attempts = None
    timeout_int = None
    def __init__(self, queue):
        Thread.__init__(self, name=binascii.hexlify(os.urandom(16)))
        self.queue = queue

    def run(self):
        while True:
            # gets the url from the queue
            output_folder, links = self.queue.get()
            # download the file
            for url in links:
                logging.info("* Thread {0} - processing URL".format(self.name))
                if not self.download_file(url,output_folder):
                    logging.error("* Thread {0} - file not loaded {1}".format(self.name,url))
            # send a signal to the queue that the job is done
            self.queue.task_done()

    #increases the timeout of the get  request library
    def on_exception_prepare_image_reload(self):
        self.timeout_int += CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS
        self.attempts += 1
        logging.info("* Tried: {num_attempts} out of: {all_attempts}".format(num_attempts=self.attempts,all_attempts=CrawlerData.ATTEMPTS_INT))
        logging.info("* Timeout: {timeout} s".format(timeout=self.timeout_int))

    def download_file(self, url,output_directory):
        """ download file """
        self.timeout_int = CrawlerData.IMPLICIT_TIMEOUT_INT_SECONDS
        status = 0
        while self.attempts < CrawlerData.ATTEMPTS_INT or status == 200:
            try:
                t_start = time.clock()
                r = requests.get(url,timeout=self.timeout_int)
                status = r.status_code
            #network errors recoverable
            except requests.exceptions.HTTPError as errh:
                logging.error("Http Error:",  exc_info=True)
                self.on_exception_prepare_image_reload()
            except requests.exceptions.ConnectionError as errc:
                logging.error("Error Connecting:",  exc_info=True)
                self.on_exception_prepare_image_reload()
            except requests.exceptions.Timeout as errt:
                logging.error("Timeout Error:",  exc_info=True)
                self.on_exception_prepare_image_reload()
            #unrecoverable error
            except requests.exceptions.RequestException as err:
                logging.error("",  exc_info=True)
                return False

            if r.status_code == 200:
                t_elapsed = time.clock() - t_start
                logging.info("* Thread: {0} Downloaded {1} in {2} seconds".format(self.name, url, str(t_elapsed)))
                fname = output_directory + '/' + os.path.basename(urllib.request.unquote(url))
                with open(fname, 'wb') as out:
                    out.write(r.content)
                return True
            else:
                logging.info("* Thread: {0} Bad URL: {1}".format(self.name, url))
                return False

class DownloadManager():
    """ Spawns dowloader threads and manages URL downloads queue """
    def __init__(self, download_dict=None, thread_count=4):
        self.thread_count = thread_count
        self.download_dict = download_dict

    def begin_downloads(self):
        """
        Start the downloader threads
        """
        self.queue = Queue()
        # Create a thread pool and give them a queue
        for i in range(self.thread_count):
            t = Downloader(self.queue)
            t.setDaemon(True)
            t.start()
        return

    def queue_image_links(self,download_dict):
        """
        fill the queue with the URLs and\n
        then feed the threads URLs via the queue
        """
        # Load the queue from the download dict
        for adv in self.download_dict:
            self.queue.put(adv)
        return
#wait for the queue to finish
    def endup_downloads(self):
        self.queue.join()
        return

