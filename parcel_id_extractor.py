# -*- coding: utf-8 -*-

"""
Fuzzes the owner search to extract all available parcel ids
"""

import os
import threading
from queue import Queue
from string import ascii_uppercase, digits
from bs4 import BeautifulSoup
import requests

SEARCH_URL = "http://qpublic9.qpublic.net/la_orleans_alsearch.php?" \
             "searchType=owner_name&INPUT={}&BEGIN={}"

Q = Queue()

class ParcelIdExtractor(object):

    def __init__(self):
         self.parcel_ids = frozenset()
         self.lock = threading.Lock()

    def update_ids(self, ids):
        """Use a lock to prevent multiple threads from updating parcel_ids"""
        self.lock.acquire()
        self.parcel_ids |= frozenset(ids)
        self.lock.release()

    def search_all_terms(self):
        """
        Puts all the search terms on a queue to be processed by worker threads.
        Note: all owner names are capitalized on the assessor's site, so we
        only use capitalized letters
        """
        # 0-9 + A-Z
        terms = [d for d in digits] + [l for l in ascii_uppercase]
        [Q.put(t) for t in terms]

    def search(self, search_term, begin=0):
        """
        Searches by owner name, extracts the parcel ids, then recursively pages
        through the results until no more ids are found for the search_term
        """
        thread = threading.current_thread().getName()
        url = SEARCH_URL.format(search_term, begin)
        print('{} searching {}'.format(thread, url))
        r = requests.get(url)
        if ('No Records Found.' in r.text):
            return
        else:
            soup = BeautifulSoup(r.text, 'html.parser')
            pids = [td.a.text for td in soup.select('td.search_value')
                    if td.a is not None and td.a.text != 'Map It']
            if (len(pids) > 0):
                self.update_ids(pids)
                self.search(search_term, begin + len(pids))

    def process_queue(self):
      while not Q.empty():
        term = Q.get()
        self.search(term)
        Q.task_done()

    def main(self, file_name='parcel_ids.txt', num_worker_threads=10):
        try:
            # populate queue with all the search terms
            self.search_all_terms()
            # start worker threads to process queue
            threads = []
            for i in range(num_worker_threads):
                t = threading.Thread(target=self.process_queue)
                threads.append(t)
                t.start()
            # wait for all threads to complete
            [t.join() for t in threads]
            with open(file_name, 'w') as f:
                print('writing {} parcel ids'.format(len(self.parcel_ids)))
                for id in self.parcel_ids:
                    f.write(id + os.linesep)
        except Exception as error:
            print(error)

if __name__ == '__main__':
    ParcelIdExtractor().main()
