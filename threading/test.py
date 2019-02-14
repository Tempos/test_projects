import threading
from queue import Queue
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from helpers import logger_call, get_links
from database import create_bd, insert_into_table, is_not_phone_exists
from constants import (RIA_PATH, RIA_RESULTS, RIA_TICKETS, RIA_NAME,
                       RIA_PROFILE, RIA_NUMBER, RIA_PRICE, RIA_ADDRESS,
                       RIA_DESCRIPTION)


# class ThreadClass(threading.Thread):
#     def __init__(self, link):
#         threading.Thread.__init__(self)
#         self.link = link
#
#     def run(self):
#         print(f"{self.getName()} says Hello World at time: {time.ctime()}")


def get_data(link):  # Gather data from tickets
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    while not queue.empty():
        # logger.info('Start looping through the links...')
        # for link in links:
        #     driver.get(link)
        #     print(f"Current thread {threading.current_thread().name}. "
        #           f"Checking link {link}")
        logger.info('Start looping through the links...')
        # for ticket in link:
        ticket = queue.get_nowait()
        driver.get(ticket)
        logger.info(f'Checking link: {ticket}')
        try:
            # Get number(s)
            phone_numbers = driver.find_elements(*RIA_NUMBER)
            numbers = []
            for number in phone_numbers:
                if number.tag_name == 'span':
                    numbers.append(
                        number.get_attribute('data-phone-number'))
            numbers = '\n'.join(numbers)
        except NoSuchElementException:
            logger.debug(f'No numbers found in link {ticket}.')
            continue
        print(numbers)

        # if is_not_phone_exists(numbers):
        #     logger.info(
        #         f'Found unique number. Gathering info from link {ticket}...')
        #     name = driver.find_element(*RIA_NAME).text
        #     address = driver.find_element(*RIA_ADDRESS).text
        #     price = driver.find_element(*RIA_PRICE).text
        #     try:
        #         profile = driver.find_element(*RIA_PROFILE) \
        #             .find_element_by_tag_name('a').get_attribute('href')
        #     except NoSuchElementException:
        #         profile = None
        #     info = driver.find_element(*RIA_DESCRIPTION).text
        #     link = driver.current_url
        #
        #     insert_into_table(numbers, name, link, price, profile, info, address)
        #     print(numbers, name, link, price, profile, info, address)
        #     logger.info(f'Information from {ticket} was stored in db.')
        # else:
        #     logger.debug('Already in the base. Skip...')

        queue.task_done()

    driver.close()


if __name__ == '__main__':
    logger = logger_call()
    links = get_links()

    start = time.time()
    thread_count = 5
    queue = Queue()

    for l in links:
        queue.put(l)

    for i in range(thread_count):
        thread = threading.Thread(target=get_data, args=(queue, ))
        thread.daemon = True
        thread.start()

    queue.join()

    # for i in range(thread_cont):
    #     t = ThreadClass(links)
    #     t.start()

    print(f"Time spent: {time.time()-start}")
