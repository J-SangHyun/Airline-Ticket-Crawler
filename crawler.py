# -*- coding: utf-8 -*-
import time
from constant import city2code
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = 'https://www.google.com/travel/flights?tfs=CBwQARoaagwIAhIIL20vMGhzcWYSCjIwMjItMDYtMjga' \
           'GhIKMjAyMi0wNy0wMnIMCAISCC9tLzBoc3FmcAGCAQsI____________AUABSAGYAQE'
XPATH_DEST = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[1]/div[1]/' \
             'div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div/div/input'
XPATH_DEST2 = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[1]/div[1]/' \
              'div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input'
XPATH_CALENDAR = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[1]/div[1]/' \
                 'div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input'
XPATH_RESET = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[1]/div[1]/' \
              'div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/button'
XPATH_ORIGIN_DATE = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[1]/div[1]/div[1]/' \
                    'div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/input'
XPATH_DEST_DATE = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[1]/div[1]/div[1]/' \
                  'div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/input'
XPATH_SUBMIT = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[1]/div[1]/div[1]/div/' \
               'div[2]/div[2]/div/div/div[2]/div/div[3]/div[3]/div/button'
XPATH_LOADING = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[2]/div[2]/div[1]'
XPATH_DIRECT = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[1]/div/div[4]/' \
               'div/div/div[2]/div[1]/div/div[1]/span/button'
XPATH_ONLY_DIRECT = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[1]/div/' \
                    'div[4]/div/div[2]/div[3]/div/div[1]/section/div[2]/div/div[2]/div/input'
XPATH_CLOSE_DIRECT = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[1]/div/div[4]/' \
                     'div/div[2]/div[3]/div/div[1]/section/div[1]/button'
XPATH_SORT = '//button[contains(., "정렬기준:")]'
XPATH_SORT_PRICE = '//li[contains(., "요금")]'
XPATH_LIST = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[2]/ul'
DELAY = 0.4
DELAY_LOAD = 2


def get_price(driver, city, date1, date2, airlines):
    driver.get(BASE_URL)
    current_prices = [-1 for _ in range(len(airlines))]
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, XPATH_DEST)))
    # click destination
    time.sleep(DELAY_LOAD)
    driver.find_element(By.XPATH, XPATH_DEST).click()
    time.sleep(DELAY)

    # input destination
    dest2 = driver.find_element(By.XPATH, XPATH_DEST2)
    dest2.send_keys(city2code[city])
    time.sleep(DELAY)
    dest2.send_keys(Keys.ENTER)
    time.sleep(DELAY)

    # open calendar
    driver.find_element(By.XPATH, XPATH_CALENDAR).click()
    time.sleep(DELAY)

    # reset calendar
    driver.find_element(By.XPATH, XPATH_RESET).click()
    time.sleep(DELAY)

    # setting origin->dest date
    origin = driver.find_element(By.XPATH, XPATH_ORIGIN_DATE)
    origin.click()
    time.sleep(DELAY)
    origin.send_keys(Keys.BACKSPACE)
    time.sleep(DELAY)
    origin.send_keys(date1)
    time.sleep(DELAY)
    origin.send_keys(Keys.ENTER)
    time.sleep(DELAY)

    # setting dest->origin date
    dest = driver.find_element(By.XPATH, XPATH_DEST_DATE)
    dest.click()
    time.sleep(DELAY)
    dest.send_keys(Keys.BACKSPACE)
    time.sleep(DELAY)
    dest.send_keys(date2)
    time.sleep(DELAY)
    dest.send_keys(Keys.ENTER)
    time.sleep(DELAY)

    # submit
    driver.find_element(By.XPATH, XPATH_SUBMIT).click()
    time.sleep(DELAY)

    # choose direct
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, XPATH_LOADING)))
    driver.find_element(By.XPATH, XPATH_DIRECT).click()
    time.sleep(DELAY)
    only_direct = driver.find_element(By.XPATH, XPATH_ONLY_DIRECT)
    try:
        WebDriverWait(driver, DELAY).until(EC.element_to_be_clickable(only_direct))
    except:
        return current_prices
    finally:
        only_direct.click()
        time.sleep(DELAY)
        driver.find_element(By.XPATH, XPATH_CLOSE_DIRECT).click()
        time.sleep(DELAY_LOAD)

        # sort
        if not driver.find_elements(By.XPATH, XPATH_LIST):
            return current_prices
        driver.find_element(By.XPATH, XPATH_SORT).click()
        time.sleep(DELAY)
        driver.find_element(By.XPATH, XPATH_SORT_PRICE).click()
        time.sleep(DELAY_LOAD)

        # get tickets
        if not driver.find_elements(By.XPATH, XPATH_LIST):
            return current_prices
        ticket_list = driver.find_element(By.XPATH, XPATH_LIST)
        tickets = ticket_list.find_elements(By.CLASS_NAME, 'JjMzFd')
        for ticket in tickets:
            name_module = ticket.find_element(By.CLASS_NAME, 'TQqf0e')
            airline_name = name_module.find_elements(By.TAG_NAME, 'span')[0].text
            if airline_name == '함께 예약된 다구간 항공권':
                airline_name = name_module.find_elements(By.TAG_NAME, 'span')[-1].text
            price_module = ticket.find_element(By.CLASS_NAME, 'U3gSDe')
            ticket_price = int(price_module.find_element(By.TAG_NAME, 'span').text.replace('₩', '').replace(',', ''))

            if airline_name in airlines:
                idx = airlines.index(airline_name)
                if current_prices[idx] == -1 or ticket_price < current_prices[idx]:
                    current_prices[idx] = ticket_price
        print(city, date1, date2, current_prices)
        return current_prices


if __name__ == '__main__':
    CHROME_DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    price = get_price(CHROME_DRIVER, '뉴욕', '07-16', '07-22', ['대한항공', '아시아나'])
    #price = get_minimum_price(CHROME_DRIVER, '서울', '도쿄', 20220801, 20220822, ['대한항공'])
    #price = get_minimum_price(CHROME_DRIVER, '서울', '도쿄', 20220622, 20220623, ['대한항공'])
    #price = get_minimum_price(CHROME_DRIVER, '서울', '도쿄', 20220801, 20220822, ['필리핀항공'])
    CHROME_DRIVER.quit()
    print(price)
