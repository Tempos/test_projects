"""Threaded version of autoria.py"""

from threading import Thread, current_thread, active_count
from queue import Queue
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from math import ceil
from time import time
from helpers import logger_call, timer
from database import (create_bd, insert_into_table, is_not_phone_exists,
                      link_exists)
from constants import (RIA_PATH, RIA_RESULTS, RIA_TICKETS, RIA_NAME,
                       RIA_PROFILE, RIA_NUMBER, RIA_PRICE, RIA_ADDRESS,
                       RIA_DESCRIPTION)


def get_links():
    """Gather ticket links"""

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    tickets_list = []
    driver.get(RIA_PATH)
    ticket_num = int(driver.find_element(*RIA_RESULTS).text.replace(' ', ''))
    page_num = ceil(ticket_num / 100)

    for page in range(page_num):
        driver.get(f'{RIA_PATH}&page={page}')
        for ticket in driver.find_elements(*RIA_TICKETS):
            url = ticket.get_attribute('href')
            if not link_exists(url):
                tickets_list.append(url)

    logger.info(f"Found {len(tickets_list)} links")
    
    return tickets_list


class GetData(Thread):
    """Gather data from links"""

    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless")

    def __init__(self, queue_of_links):
        Thread.__init__(self)
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.queue = queue_of_links

    def run(self):
        logger.info(current_thread().name + " started")

        while not self.queue.empty():
            ticket = self.queue.get()
            self.driver.get(ticket)

            try:    # Get number(s)
                numbers = []
                phone_numbers = self.driver.find_elements(*RIA_NUMBER)
                for number in phone_numbers:
                    if number.tag_name == 'span':
                        numbers.append(
                            number.get_attribute('data-phone-number'))
                numbers = '\n'.join(numbers)
            except NoSuchElementException:
                logger.debug(f'No numbers found in link {ticket}.')
                continue

            try:    # Get profile link
                profile = self.driver.find_element(*RIA_PROFILE)\
                    .find_element_by_tag_name('a').get_attribute('href')
            except NoSuchElementException:
                profile = None

            queue_out.put(
                (numbers,
                 self.driver.find_element(*RIA_NAME).text,
                 self.driver.current_url,
                 self.driver.find_element(*RIA_PRICE).text,
                 profile,
                 self.driver.find_element(*RIA_DESCRIPTION).text,
                 self.driver.find_element(*RIA_ADDRESS).text)
            )

            logger.info(current_thread().name + " - Information from " + ticket
                        + " was put in queue_out.")
            self.queue.task_done()

        self.driver.close()
        logger.info(current_thread().name + " run finished.")


class StoreData(Thread):
    """ Store unique data in DB"""

    def __init__(self, data):
        Thread.__init__(self)
        self.queue = data

    def run(self):
        while not self.queue.empty() or active_count() > 0:
            stored_data = self.queue.get()

            if is_not_phone_exists(stored_data[0]):
                logger.info(current_thread().name
                            + " - Found unique number. Storing info in db..."
                            + stored_data[2])
                insert_into_table(*stored_data)
            else:
                logger.debug('Already in the base. Skip...')

            self.queue.task_done()

        logger.info(current_thread().name + " run finished")


if __name__ == '__main__':
    logger = logger_call()
    queue, queue_out = Queue(), Queue()
    create_bd()

    links = get_links()
    start = time()
    thread_count = 5

    # Populate queue
    for link in links:
        queue.put(link)

    # Create threads for links parsing
    for _ in range(thread_count):
        t = GetData(queue)
        t.daemon = True
        t.start()

    # Create thread for data storing to db
    db_thread = StoreData(queue_out)
    db_thread.daemon = True
    db_thread.name = 'Thread-DB'
    db_thread.start()

    queue.join()
    queue_out.join()

    # Measure time spent
    logger.info("Time spent: " + timer(start, time()))
