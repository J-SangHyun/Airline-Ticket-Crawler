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

BASE_URL = 'https://www.google.com/travel/flights/en?hl=kr&gl=KR&curr=KRW'
XPATH_ORIGIN = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[1]/div[1]/div[1]/' \
               'div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input'
XPATH_ORIGIN2 = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[1]/div[1]/div[1]/' \
                'div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input'
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
XPATH_AIRLINE = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[1]/div/div[4]/' \
                'div/div/div[2]/div[1]/div/div[2]/span/button'
XPATH_CLOSE_AIRLINE = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[1]/div/div[4]/' \
                      'div/div[2]/div[3]/div/div[1]/section/div[1]/button'
XPATH_SORT = '//button[contains(., "정렬기준:")]'
XPATH_SORT_PRICE = '//li[contains(., "요금")]'
XPATH_LIST = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/c-wiz/div[2]/div[2]/ul'
XPATH_PRICE = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[2]/span'
DELAY = 0.5


def get_price(driver, origin_city, city, date1, date2, airlines):
    driver.get(BASE_URL)
    current_prices = [-1 for _ in range(len(airlines))]
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, XPATH_DEST)))
    time.sleep(2 * DELAY)

    # input destination
    driver.find_element(By.XPATH, XPATH_ORIGIN).click()
    time.sleep(DELAY)
    origin2 = driver.find_element(By.XPATH, XPATH_ORIGIN2)
    origin2.send_keys(origin_city)
    time.sleep(DELAY)
    origin2.send_keys(Keys.ENTER)
    time.sleep(DELAY)

    # click destination
    driver.find_element(By.XPATH, XPATH_DEST).click()
    time.sleep(DELAY)
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
        only_direct.click()
    except:
        return current_prices
    finally:
        time.sleep(DELAY)
        driver.find_element(By.XPATH, XPATH_CLOSE_DIRECT).click()
        while driver.find_element(By.CLASS_NAME, 'Jwkq3b').get_attribute('class') != 'Jwkq3b':
            time.sleep(DELAY)
        time.sleep(DELAY)

        # sort
        if not driver.find_elements(By.XPATH, XPATH_LIST):
            return current_prices
        driver.find_element(By.XPATH, XPATH_SORT).click()
        time.sleep(DELAY)
        driver.find_element(By.XPATH, XPATH_SORT_PRICE).click()
        time.sleep(4 * DELAY)

        # choose airline
        for i in range(len(airlines)):
            airline = airlines[i]
            driver.find_element(By.XPATH, XPATH_AIRLINE).click()
            time.sleep(DELAY)
            if not driver.find_elements(By.XPATH, f'//button[@data-value="{airline}"]'):
                continue
            driver.find_element(By.XPATH, f'//button[@data-value="{airline}"]').click()
            time.sleep(DELAY)
            driver.find_element(By.XPATH, XPATH_CLOSE_AIRLINE).click()
            time.sleep(4 * DELAY)

            # get tickets
            if not driver.find_elements(By.XPATH, XPATH_LIST):
                continue
            ticket_list = driver.find_element(By.XPATH, XPATH_LIST)
            tickets = ticket_list.find_elements(By.CLASS_NAME, 'JjMzFd')
            for ticket in tickets:
                name_module = ticket.find_element(By.CLASS_NAME, 'TQqf0e')
                airline_name = name_module.find_elements(By.TAG_NAME, 'span')[0].text
                if '다구간 항공권' in airline_name:
                    airline_name = name_module.find_elements(By.TAG_NAME, 'span')[-1].text
                if airline != airline_name:
                    continue
                ticket.click()
                time.sleep(3 * DELAY)
                break

            # get dest tickets
            if not driver.find_elements(By.XPATH, XPATH_LIST):
                continue
            dest_ticket_list = driver.find_element(By.XPATH, XPATH_LIST)
            dest_tickets = dest_ticket_list.find_elements(By.CLASS_NAME, 'JjMzFd')
            for ticket in dest_tickets:
                name_module = ticket.find_element(By.CLASS_NAME, 'TQqf0e')
                airline_name = name_module.find_elements(By.TAG_NAME, 'span')[0].text
                if '다구간 항공권' in airline_name:
                    airline_name = name_module.find_elements(By.TAG_NAME, 'span')[-1].text
                if airline != airline_name:
                    continue
                ticket.click()
                time.sleep(3 * DELAY)
                break

            while driver.find_element(By.CLASS_NAME, 'Jwkq3b').get_attribute('class') != 'Jwkq3b s2h5lc':
                time.sleep(DELAY)
            time.sleep(DELAY)

            for _ in range(10):
                try:
                    ticket_price_text = driver.find_element(By.XPATH, XPATH_PRICE).text
                    ticket_price = int(ticket_price_text.replace('₩', '').replace(',', ''))
                    current_prices[i] = ticket_price
                except:
                    time.sleep(DELAY)
                    continue
                finally:
                    break
            driver.back()
            driver.back()
            time.sleep(2 * DELAY)

        print(origin_city, city, date1, date2, current_prices)
        return current_prices


if __name__ == '__main__':
    CHROME_DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    price = get_price(CHROME_DRIVER, '서울특별시', '도쿄', '06-24', '06-27', ['대한항공', '아시아나'])
    #price = get_minimum_price(CHROME_DRIVER, '서울', '도쿄', 20220801, 20220822, ['대한항공'])
    #price = get_minimum_price(CHROME_DRIVER, '서울', '도쿄', 20220622, 20220623, ['대한항공'])
    #price = get_minimum_price(CHROME_DRIVER, '서울', '도쿄', 20220801, 20220822, ['필리핀항공'])
    CHROME_DRIVER.quit()
    print(price)
