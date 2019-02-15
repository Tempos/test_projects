import threading
from queue import Queue
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from math import ceil
import time
from helpers import logger_call
from database import (create_bd, insert_into_table, is_not_phone_exists,
                      link_exists)
from constants import (RIA_PATH, RIA_RESULTS, RIA_TICKETS, RIA_NAME,
                       RIA_PROFILE, RIA_NUMBER, RIA_PRICE, RIA_ADDRESS,
                       RIA_DESCRIPTION)

logger = logger_call()
locker = threading.Lock()
queue = Queue()
queue_out = Queue()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)


def get_links():
    """Gather ticket links"""

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


class GetNumbers(threading.Thread):
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless")

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.queue = queue

    def run(self):
        logger.info(f"Started run on {threading.current_thread().name}.")
        while not self.queue.empty():
            ticket = self.queue.get()
            self.driver.get(ticket)

            try:
                # Get number(s)
                phone_numbers = self.driver.find_elements(*RIA_NUMBER)
                numbers = []
                for number in phone_numbers:
                    if number.tag_name == 'span':
                        numbers.append(
                            number.get_attribute('data-phone-number'))
                numbers = '\n'.join(numbers)
            except NoSuchElementException:
                logger.debug(f'No numbers found in link {ticket}.')
                continue

            # if is_not_phone_exists(numbers):
            #     logger.info(
            #         f'Found unique number. Gathering info from a link {ticket}')
            #     try:
            #         profile = driver.find_element(*RIA_PROFILE) \
            #             .find_element_by_tag_name('a').get_attribute('href')
            #     except NoSuchElementException:
            #         profile = None
            #
            #     insert_into_table(numbers,
            #                       driver.find_element(*RIA_NAME).text,
            #                       driver.current_url,
            #                       driver.find_element(*RIA_PRICE).text,
            #                       profile,
            #                       driver.find_element(*RIA_DESCRIPTION).text,
            #                       driver.find_element(*RIA_ADDRESS).text)
            #     logger.info(f'Information from {ticket} was stored in db.')
            # else:
            #     logger.debug('Already in the base. Skip...')

            queue_out.put((numbers, ticket))
            self.queue.task_done()

            # Todo: Clean this part
            first_num = numbers.split('\n')[0]
            logger.info(threading.current_thread().name + ": " + first_num +
                        " added to 'queue_out'.")

        self.driver.close()
        logger.info(threading.current_thread().name + " class run finished.")


# Todo: Get data from queue_out and store it in db.
class GetData(threading.Thread):
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless")

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            queue_item = self.queue.get()
            numbers, ticket = queue_item

            if is_not_phone_exists(numbers):
                logger.info(
                    f'Found unique number. Gathering info from a link {ticket}')
                try:
                    profile = driver.find_element(*RIA_PROFILE) \
                        .find_element_by_tag_name('a').get_attribute('href')
                except NoSuchElementException:
                    profile = None

                insert_into_table(numbers,
                                  driver.find_element(*RIA_NAME).text,
                                  driver.current_url,
                                  driver.find_element(*RIA_PRICE).text,
                                  profile,
                                  driver.find_element(*RIA_DESCRIPTION).text,
                                  driver.find_element(*RIA_ADDRESS).text)
                logger.info(f'Information from {ticket} was stored in db.')
            else:
                logger.debug('Already in the base. Skip...')

            self.queue.task_done()
        logger.info("class GetData finished")

    # def db_io(numbers):
    #     if is_not_phone_exists(numbers):
    #         logger.info(
    #             f'Found unique number. Gathering info from link {ticket}...')
    #     insert_into_table(numbers, name, link, price, profile, info, address)


# def get_data(data):  # Gather data from tickets
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--incognito")
#     chrome_options.add_argument("--headless")
#     driver = webdriver.Chrome(chrome_options=chrome_options)
#
#     while not queue_out.empty():
#         logger.info('Start looping through the links...')
#         ticket = queue_out.get_nowait()
#         driver.get(link)
#         logger.info(f"Current thread {threading.current_thread().name}.")
#
#         for ticket in link:
#             ticket = queue.get_nowait()
#             driver.get(ticket)
#         try:
#             # Get number(s)
#             phone_numbers = driver.find_elements(*RIA_NUMBER)
#             numbers = []
#             for number in phone_numbers:
#                 if number.tag_name == 'span':
#                     numbers.append(
#                         number.get_attribute('data-phone-number'))
#             numbers = '\n'.join(numbers)
#         except NoSuchElementException:
#             logger.debug(f'No numbers found in link {ticket}.')
#             continue
#
#         if is_not_phone_exists(numbers):
#             logger.info(
#                 f'Found unique number. Gathering info from link {ticket}...')
#             try:
#                 profile = driver.find_element(*RIA_PROFILE) \
#                     .find_element_by_tag_name('a').get_attribute('href')
#             except NoSuchElementException:
#                 profile = None
#
#             insert_into_table(numbers,
#                               driver.find_element(*RIA_NAME).text,
#                               driver.current_url,
#                               driver.find_element(*RIA_PRICE).text,
#                               profile,
#                               driver.find_element(*RIA_DESCRIPTION).text,
#                               driver.find_element(*RIA_ADDRESS).text)
#             logger.info(f'Information from {ticket} was stored in db.')
#         else:
#             logger.debug('Already in the base. Skip...')
#
#         queue.task_done()
#     driver.close()


if __name__ == '__main__':

    create_bd()

    links = get_links()
    start = time.time()
    thread_count = 2

    # Populate queue
    for link in links:
        queue.put(link)

    # Create threads for links parsing
    for _ in range(thread_count):
        t = GetNumbers(queue)
        t.daemon = True
        t.start()

    queue.join()

    db_thread = GetData(queue_out)
    db_thread.daemon = True
    db_thread.start()
    db_thread.join()    # Not important

    queue_out.join()

    print(f"Time spent: {time.time()-start}")
