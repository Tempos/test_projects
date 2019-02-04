from selenium import webdriver
from constants import *

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()


def find_links():
    driver.get(f'{URL_PATH}&page={PAGE}')
    ticket_num = int(driver.find_element(*RESULTS_NUM).text)
    page, lst = PAGE, []
    while driver.find_element(*NEXT_PAGE).get_attribute('href') != 'javascript:void(0)':
        for i in range(1, SIZE + 1):
            ticket = driver.find_element_by_xpath(f"""//*[@id="searchResults"]
                                /section[{i}]/div[4]/div[2]/div[1]/div/a""").get_attribute('href')
            lst.append(ticket)
        page += 1
        driver.get(f'{URL_PATH}&page={page}')

    last = ticket_num - len(lst)
    for i in range(1, last + 1):
        ticket = driver.find_element_by_xpath(f"""//*[@id="searchResults"]
                            /section[{i}]/div[4]/div[2]/div[1]/div/a""").get_attribute('href')
        lst.append(ticket)
    return lst
    # print(page, len(links), links)


def gather_data():
    # Get numbers
    driver.get('https://auto.ria.com/auto_rolls_royce_ghost_22218703.html#prevAuto=22811000')
    nums = driver.find_elements_by_class_name('phone')
    numbers = []
    for elem in nums:
        if elem.tag_name == 'span':
            numbers.append(elem.get_attribute('data-phone-number'))
    # Get name
    name = driver.find_element(*NAME).text
    # Get address
    address = driver.find_element(*ADDRESS).text
    # Get price
    price = driver.find_element(*PRICE).text
    # Get info
    info = driver.find_element(*DESCRIPTION).text
    # Get link
    link = driver.current_url

    print(f'{name}\n{numbers}\n{address}\n{price}\n{info}\n{link}')

gather_data()


# links = find_links()
# for item in links:
#     print(item)
# print(len(links))

driver.close()
