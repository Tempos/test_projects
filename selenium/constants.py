""" Constants for LINKS and paths. """
from selenium.webdriver.common.by import By

# URL_PATH' variables
PAGE = 0
SIZE = 20

URL_PATH = f"""https://auto.ria.com/search/
?body.id[0]=3
&categories.main.id=1
&price.USD.gte=200000
&price.currency=1
&abroad.not=0
&custom.not=1
&size={SIZE}
"""

RESULTS_NUM = (By.XPATH, '//*[@id="staticResultsCount"]')
TICKET_PATH = (By.XPATH, '//*[@id="searchResults"]/section[1]/div[4]/div[2]/div[1]/div/a')
NEXT_PAGE = (By.XPATH, '//*[@id="searchPagination"]/div/nav/span[11]/a')

# Ticket details
NAME = (By.XPATH, '//*[@id="userInfoBlock"]/div[1]/div/h4')
NUMBER = (By.XPATH, '//*[@id="userInfoBlock"]/div[2]/div[1]/span/a[2]')
PRICE = (By.XPATH, '//*[@id="showLeftBarView"]/section[1]/div[1]/strong')
ADDRESS = (By.XPATH, '//*[@id="userInfoBlock"]/ul[1]/li[1]/div/a')
DESCRIPTION = (By.XPATH, '//*[@id="heading-cars"]/div/h1')
