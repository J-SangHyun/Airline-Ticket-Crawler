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


def get_url(port1, port2, date1, date2):
    return DETAILED_URL % (port1, port2, date1, port2, port1, date2)


def get_price(driver, url, airline):
    driver.get(url)
    current_price = -1
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'inlineFilter_inner__1DuQ7'))
        )
    finally:
        if driver.find_elements(By.CLASS_NAME, 'concurrent_ConcurrentItemContainer__2lQVG'):
            driver.find_element(By.XPATH, '//button[@class="inlineFilter_Tag__97qqq"][normalize-space()="요금조건"]').click()
            time.sleep(0.1)
            driver.find_element(By.XPATH, '//button[@class="checkbox"][normalize-space()="성인"]').click()
            time.sleep(0.1)
            driver.find_element(By.XPATH, '//button[@class="tab"][normalize-space()="항공사"]').click()
            time.sleep(0.1)
            if not driver.find_elements(By.XPATH, f'//button[@class="checkbox"][normalize-space()="{airline}"]'):
                return current_price
            driver.find_element(By.XPATH, f'//button[@class="checkbox"][normalize-space()="{airline}"]').click()
            time.sleep(0.1)
            driver.find_element(By.XPATH, f'//button[@class="submit"]').click()
            time.sleep(0.1)

            tickets = driver.find_elements(By.CLASS_NAME, 'concurrent_ConcurrentItemContainer__2lQVG')
            for ticket in tickets:
                if ticket.find_elements(By.CLASS_NAME, 'concurrent_RoundSameAL__1Y3j3'):
                    current_price = int(ticket.find_element(By.CLASS_NAME, 'item_num__3R0Vz').text.replace(',', ''))
    return current_price


def get_minimum_price(driver, city1, city2, date1, date2, airline):
    minimum_price = -1
    for port1 in city2code[city1]:
        for port2 in city2code[city2]:
            url = get_url(port1, port2, date1, date2)
            print(url)
            _price = get_price(driver, url, airline)
            print(f'[{port1}]->[{port2}]->[{port1}] 최저가 : {_price}원')
            if minimum_price == -1 or _price < minimum_price:
                minimum_price = _price
    return minimum_price


if __name__ == '__main__':
    CHROME_DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    price = get_minimum_price(CHROME_DRIVER, '서울', '오사카', '20220801', '20220822', '아시아나항공')
    #price = get_minimum_price(CHROME_DRIVER, '서울', '도쿄', 20220801, 20220822, '대한항공')
    #price = get_minimum_price(CHROME_DRIVER, '서울', '도쿄', 20220622, 20220623, '대한항공')
    #price = get_minimum_price(CHROME_DRIVER, '서울', '도쿄', 20220801, 20220822, '필리핀항공')
    CHROME_DRIVER.quit()
    print(price)
