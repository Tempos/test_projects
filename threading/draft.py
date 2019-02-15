# Gather data from tickets
for ticket in tickets_list:
    driver.get(ticket)
    logger.info(f'Checking link: {ticket}')
    try:
        # Get number(s)
        phone_numbers = driver.find_elements(*RIA_NUMBER)
        numbers = []
        for number in phone_numbers:
            if number.tag_name == 'span':
                numbers.append(number.get_attribute('data-phone-number'))
        numbers = '\n'.join(numbers)
    except NoSuchElementException:
        logger.debug(f'No numbers found in link {ticket}.')
        continue

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


querry.join()
out_querry.join()
thread.stop()
