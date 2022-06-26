# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = 'https://www.hotelscombined.co.kr/flights'

# XPath
XPATH_OK = '/html/body/div[10]/div/div[3]/div/div/div/div[2]/button'
XPATH_PROGRESS = '/html/body/div[1]/div[1]/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div'
XPATH_PRICE = '/html/body/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[3]' \
              '/div[2]/div[2]/div/div/div/div[1]/a[1]'
XPATH_ONLY = '/html/body/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/div[5]/' \
             'div/div[3]/div/div[1]/div[2]/ul/'

DELAY = 0.3


def get_price(driver, origin_city, dest_city, date1, date2, airlines):
    current_prices = [-1 for _ in range(len(airlines))]
    URL = f'{BASE_URL}/{origin_city}-{dest_city}/{date1}/{date2}?sort=price_a&fs=stops=~0'
    driver.get(URL)

    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, XPATH_PROGRESS)))
    except:
        time.sleep(DELAY)
    else:
        loading = False
        while (not loading) or driver.find_element(By.XPATH, XPATH_PROGRESS).get_attribute('aria-valuenow') != '0':
            if (not loading) and float(driver.find_element(By.XPATH, XPATH_PROGRESS).get_attribute('aria-valuenow')) > 0:
                loading = True
            time.sleep(DELAY)

    # ad removal
    if driver.find_elements(By.XPATH, XPATH_OK):
        driver.find_element(By.XPATH, XPATH_OK).click()
        time.sleep(DELAY)

    # only specific airline
    for i in range(len(airlines)):
        if not driver.find_elements(By.XPATH, XPATH_ONLY + f'li[contains(., "{airlines[i]}")]'):
            continue

        airline_li = driver.find_element(By.XPATH, XPATH_ONLY + f'li[contains(., "{airlines[i]}")]')
        time.sleep(DELAY)
        if not airline_li.find_elements(By.XPATH, 'div/div[2]/button[2]'):
            continue

        price_text = airline_li.find_element(By.XPATH, 'div/div[2]/button[2]').text
        if not price_text:
            continue
        current_prices[i] = int(price_text.replace('원', '').replace(',', ''))

    print(origin_city, dest_city, date1, date2, current_prices)
    return current_prices


if __name__ == '__main__':
    CHROME_DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    price = get_price(CHROME_DRIVER, 'SEL', 'NRT', '2022-07-22', '2022-07-30', ['대한항공', '아시아나'])
    CHROME_DRIVER.quit()
    print(price)
