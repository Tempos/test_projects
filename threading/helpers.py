import logging
from constants import LOG_NAME
from selenium import webdriver
from math import ceil
from constants import (RIA_PATH, RIA_RESULTS, RIA_TICKETS, RIA_NAME,
                       RIA_PROFILE, RIA_NUMBER, RIA_PRICE, RIA_ADDRESS,
                       RIA_DESCRIPTION)


def number_format(num):
    num = num.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
    if num.startswith('0'):
        num = '38' + num
    return num


def logger_call():
    """ Configure our logger """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s -- %(module)s -- %(levelname)s -- %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S')

    # Save log to file
    file_handler = logging.FileHandler(LOG_NAME)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Show log in console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def get_links():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # Gather ticket links
    tickets_list = []
    driver.get(RIA_PATH)
    ticket_num = int(driver.find_element(*RIA_RESULTS).text.replace(' ', ''))
    page_num = ceil(ticket_num / 100)
    for page in range(page_num):
        driver.get(f'{RIA_PATH}&page={page}')
        for ticket in driver.find_elements(*RIA_TICKETS):
            tickets_list.append(ticket.get_attribute('href'))
    print(f"Found {len(tickets_list)} links")
    return tickets_list


class ElementHasAttribute(object):
    """An expectation for checking that an element has a particular attribute.

    returns the WebElement once it has the particular attribute
    """

    def __init__(self, locator, attribute_name, attribute_value):
        self.locator = locator
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value

    def __call__(self, driver):
        element = driver.find_element(*self.locator)  # Finding the referenced element
        if self.attribute_value in element.get_attribute(self.attribute_name):
            return element
        else:
            return False
