# -*- coding: utf-8 -*-
from tqdm import tqdm
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
from crawler import get_minimum_price
from constant import cityEurope, cityAmerica


if __name__ == '__main__':
    CHROME_DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    workbook = Workbook()
    today = date.today()
    day_list = ['일', '월', '화', '수', '목', '금', '토']
    #city_list = ['도쿄', '괌', '오사카', '뉴욕', '런던']
    #airline_list = ['대한한공', '제주항공', '아시아나항공', '진에어']
    city_list = ['도쿄']
    airline_list = ['대한항공', '아시아나항공']

    sheet = workbook.active
    sheet.title = today.strftime('%Y%m%d')
    sheet.cell(row=2, column=2, value='출발일')
    workbook.save(f'./{today.strftime("%Y%m%d")}.xlsx')

    for i in range(len(city_list)):
        sheet.cell(column=3+i*len(airline_list), row=1, value=city_list[i])
        sheet.merge_cells(start_column=3+i*len(airline_list), start_row=1,
                          end_column=2+(i+1)*len(airline_list), end_row=1)
        for j in range(len(airline_list)):
            sheet.cell(column=3+i*len(airline_list)+j, row=2, value=airline_list[j])
    workbook.save(f'./{today.strftime("%Y%m%d")}.xlsx')

    for tqdm_i in tqdm(range(len(city_list) * 3 * 7)):
        i = tqdm_i // (3 * 7)
        j = (tqdm_i % (3 * 7)) // 7
        k = tqdm_i % 7

        city = city_list[i]
        period = 6 if (city in cityEurope or city in cityAmerica) else 3
        date1 = today + timedelta(days=28*j+k)
        date2 = date1 + timedelta(days=period)
        prices = get_minimum_price(CHROME_DRIVER, '서울', city,
                                   date1.strftime("%Y%m%d"), date2.strftime("%Y%m%d"), airline_list)
        cell_row = 3 + 7*j + k
        sheet.cell(column=2, row=cell_row, value=f'{int(date1.strftime("%Y"))}년 '
                                                 f'{int(date1.strftime("%m"))}월 '
                                                 f'{int(date1.strftime("%d"))}일 '
                                                 f'{day_list[int(date1.strftime("%w"))]}요일')

        for l in range(len(airline_list)):
            cell_column = 3 + i * len(airline_list) + l
            price = prices[l]
            if price != -1:
                sheet.cell(column=cell_column, row=cell_row, value=prices[l])
        workbook.save(f'./{today.strftime("%Y%m%d")}.xlsx')

    workbook.save(f'./{today.strftime("%Y%m%d")}.xlsx')
    CHROME_DRIVER.quit()
