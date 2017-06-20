'''
    City to collect data from: Tampa FL
    url = https://aca.tampagov.net/CitizenAccess/
'''

import requests
from bs4 import BeautifulSoup
import random
from pprint import pprint
import time
import sqlite3

###############################
### selenium module imports ###
###############################

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

conn = sqlite3.connect("python_meetup.sqlite")
cur = conn.cursor()
table_name = "python_meetup_table"
cur.execute("DROP TABLE IF EXISTS " + table_name)
cur.execute("""CREATE TABLE {} (
            permit_no varchar(255),
            status varchar(255),
            address varchar(255),
            description varchar(1555),
            valuation varchar(255),
            parcel varchar(1255)
        );
    """.format(table_name))

def init_driver():
    driver = webdriver.Chrome("/Users/davidmorrison/Downloads/chromedriver")
    driver.wait = WebDriverWait(driver, 30)
    return driver

def scrape(driver, search_term, start_date, end_date):
    initial_url = 'https://aca.tampagov.net/CitizenAccess' + \
                  '/Cap/CapHome.aspx?module=Building&TabName=Building'
    driver.get(initial_url)
    time.sleep(random.random() * 5)
    SELECT_PERMIT = 'ctl00$PlaceHolderMain$generalSearchForm$ddlGSPermitType'
    driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='{}']/option[text()='{}']".format(SELECT_PERMIT,search_term)))).click()
    time.sleep(random.random() * 5)
    START_DATE = 'ctl00$PlaceHolderMain$generalSearchForm$txtGSStartDate'
    driver.wait.until(EC.element_to_be_clickable((By.NAME, START_DATE))).send_keys("{}".format(start_date))
    time.sleep(random.random() * 5)
    END_DATE = 'ctl00$PlaceHolderMain$generalSearchForm$txtGSEndDate'
    driver.wait.until(EC.element_to_be_clickable((By.NAME, END_DATE))).send_keys("{}".format(end_date))
    time.sleep(random.random() * 5)
    CLICK_BUTTON = 'ctl00_PlaceHolderMain_btnNewSearch'
    driver.wait.until(EC.element_to_be_clickable((By.ID, CLICK_BUTTON))).click()
    time.sleep(10)

    while True:
        #extract links and scrape data
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for a in soup.find_all('a', href=True):
            url = 'https://aca.tampagov.net' + a['href']
            # pattern in urls that have data that we need
            # is Cap/CapDetail, so lets search for that in urls
            if 'Cap/CapDetail' in url:
                response = requests.get(url)
                soup = BeautifulSoup(response.text)
                span = soup.find_all('span')
                span = [" ".join(s.get_text().split()).replace("'", " ").replace("\n", "") for s in span]
                try:
                    permit_no = [span[i+1] 
                                     for i, x in enumerate(span)
                                     if 'Record' in x][0]
                    if not permit_no:
                        permit_no = ""
                    status = [span[i+1]
                              for i, x in enumerate(span)
                              if 'Record Status:' in x][1]
                    if not status:
                        status = ""
                    address = [span[i+4].replace(" T ", " Tampa, FL ")
                               for i, x in enumerate(span)
                               if 'Work Location' in x][1]
                    if not address:
                        address = ""
                    description = [span[i+1]
                                   for i, x in enumerate(span)
                                   if 'Project Description:' in x][0]
                    if not description:
                        description = ""
                    valuation = [span[i+1]
                                 for i, x in enumerate(span)
                                 if 'Job Value:' in x][1]
                    if not valuation:
                        valuation = ""
                    parcel = [x.replace("Parcel Information Parcel Number:", "")
                                    for x in span
                                    if 'Parcel Information Parcel Number:' in x][0]
                    if not parcel:
                        parcel = ""
                    #insert values into db
                    print("Permit Number: " + permit_no)
                    print("address: " + address)
                    print("status: " + status)
                    print("description: " + description)
                    print("parcel: " + parcel[0:21])
                    print("-" * 100)
                    cur.execute("""INSERT INTO {0}
                                    VALUES('{1}','{2}','{3}','{4}','{5}','{6}');
                                    """.format(
                                            table_name,
                                            permit_no,
                                            status,
                                            address,
                                            description,
                                            valuation,
                                            parcel[0:21],
                    ))
                    conn.commit()
                except:
                    pass

        #iterate over all pages by clicking the next button
        try:
            next_page = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='{}']".format('Next >'))))
        except Exception as ex:
            our_exception = "An exception of type {0} occured."
            message = our_exception.format(type(ex).__name__)
            print(message)
            break
        next_page.click()

if __name__ == "__main__":
    driver = init_driver()
    scrape = scrape(driver,
                   'Residential Roof Trade Permit', 
                   '01/25/2017',
                   '04/04/2017')
    driver.quit()
