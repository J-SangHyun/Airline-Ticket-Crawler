# -*- coding: utf-8 -*-
import time
from constant import city2code
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = 'https://flight.naver.com/flights/international/'
DETAILED_URL = BASE_URL + '%s-%s-%s/%s-%s-%s?adult=1&isDirect=true&fareType=Y&selectType=concurrent'
DELAY = 0.1


def get_url(port1, port2, date1, date2):
    return DETAILED_URL % (port1, port2, date1, port2, port1, date2)


def get_price(driver, url, airlines):
    driver.get(url)
    current_prices = [-1 for _ in range(len(airlines))]
    try:
        WebDriverWait(driver, 40).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'inlineFilter_inner__1DuQ7'))
        )
    finally:
        if driver.find_elements(By.CLASS_NAME, 'concurrent_ConcurrentItemContainer__2lQVG'):
            driver.find_element(By.XPATH,
                                '//button[@class="inlineFilter_Tag__97qqq"][normalize-space()="요금조건"]').click()
            time.sleep(DELAY)
            driver.find_element(By.XPATH, '//button[@class="checkbox"][normalize-space()="성인"]').click()
            time.sleep(DELAY)
            driver.find_element(By.XPATH, f'//button[@class="submit"]').click()
            time.sleep(DELAY)

            for i in range(len(airlines)):
                airline = airlines[i]
                driver.find_element(By.XPATH,
                                    '//button[@class="inlineFilter_Tag__97qqq"][contains(., "항공사")]').click()
                time.sleep(DELAY)
                driver.find_element(By.XPATH, '//button[@class="checkbox as_all"][normalize-space()="전체"]').click()
                time.sleep(DELAY)
                if not driver.find_elements(By.XPATH, f'//button[@class="checkbox"][normalize-space()="{airline}"]'):
                    current_prices[i] = -1
                    driver.find_element(By.XPATH, f'//button[@class="submit"]').click()
                    time.sleep(DELAY)
                    continue
                driver.find_element(By.XPATH, f'//button[@class="checkbox"][normalize-space()="{airline}"]').click()
                time.sleep(DELAY)
                driver.find_element(By.XPATH, f'//button[@class="submit"]').click()
                time.sleep(DELAY)

                tickets = driver.find_elements(By.CLASS_NAME, 'concurrent_ConcurrentItemContainer__2lQVG')
                for ticket in tickets:
                    if ticket.find_elements(By.CLASS_NAME, 'concurrent_RoundSameAL__1Y3j3'):
                        current_price = int(ticket.find_element(By.CLASS_NAME, 'item_num__3R0Vz').text.replace(',', ''))
                        current_prices[i] = current_price
                        break
                time.sleep(DELAY)
    return current_prices


def get_minimum_price(driver, city1, city2, date1, date2, airlines):
    minimum_prices = [-1 for _ in range(len(airlines))]
    for port1 in city2code[city1]:
        for port2 in city2code[city2]:
            url = get_url(port1, port2, date1, date2)
            _prices = get_price(driver, url, airlines)
            time.sleep(2)
            for i in range(len(airlines)):
                if minimum_prices[i] == -1 or _prices[i] < minimum_prices[i]:
                    minimum_prices[i] = _prices[i]
    return minimum_prices


if __name__ == '__main__':
    CHROME_DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    price = get_minimum_price(CHROME_DRIVER, '서울', '도쿄', '20220608', '20220611', ['대한항공', '아시아나항공'])
    #price = get_minimum_price(CHROME_DRIVER, '서울', '도쿄', 20220801, 20220822, ['대한항공'])
    #price = get_minimum_price(CHROME_DRIVER, '서울', '도쿄', 20220622, 20220623, ['대한항공'])
    #price = get_minimum_price(CHROME_DRIVER, '서울', '도쿄', 20220801, 20220822, ['필리핀항공'])
    CHROME_DRIVER.quit()
    print(price)
