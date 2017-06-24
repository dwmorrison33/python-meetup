'''
    City to collect data from: Sacramento, CA
    https://aca.accela.com/sacramento/Default.aspx
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
            date varchar(255),
            permit_no varchar(255),
            record_type varchar(255),
            description varchar(1555),
            address varchar(255),
            status varchar(255)
        );
    """.format(table_name))

def init_driver():
    driver = webdriver.Chrome("/Users/davidmorrison/Downloads/chromedriver")
    driver.wait = WebDriverWait(driver, 30)
    return driver

def scrape(driver, search_term, start_date, end_date):
    initial_url = 'https://aca.accela.com/sacramento/Default.aspx'
    driver.get(initial_url)
    time.sleep(random.random() * 10)
    driver.switch_to.default_content()
    driver.switch_to_frame("ACAFrame")
    CLICK_BUILDING = 'ctl00_PlaceHolderMain_TabDataList_TabsDataList_ctl00_LinksDataList_ctl00_LinkItemUrl'
    driver.wait.until(EC.element_to_be_clickable((By.ID, CLICK_BUILDING))).click()
    time.sleep(random.random() * 5)
    START_DATE = 'ctl00$PlaceHolderMain$generalSearchForm$txtGSStartDate'
    driver.wait.until(EC.element_to_be_clickable((By.NAME, START_DATE))).send_keys("{}".format(start_date))
    time.sleep(random.random() * 5)
    END_DATE = 'ctl00$PlaceHolderMain$generalSearchForm$txtGSEndDate'
    driver.wait.until(EC.element_to_be_clickable((By.NAME, END_DATE))).send_keys("{}".format(end_date))
    time.sleep(random.random() * 5)
    PROJECT_NAME = 'ctl00$PlaceHolderMain$generalSearchForm$txtGSProjectName'
    driver.wait.until(EC.element_to_be_clickable((By.NAME, PROJECT_NAME))).send_keys("{}".format(search_term))
    time.sleep(random.random() * 5)
    CLICK_BUTTON = 'ctl00_PlaceHolderMain_btnNewSearch'
    driver.wait.until(EC.element_to_be_clickable((By.ID, CLICK_BUTTON))).click()
    time.sleep(10)

    pageno = 2
    while True:
        # lets extract the data with BeautifulSoup Now
        soup = BeautifulSoup(driver.page_source, "html.parser")
        even_rows = soup.find_all("tr", class_="ACA_TabRow_Even ACA_TabRow_Even_FontSize")
        for row in even_rows:
            td = row.find_all('td')
            value = [t.get_text().replace("\n", "").replace("'", "")  for t in td]
            if value:
                # instead of just inserting into table with index,  
                # lets assign them to a variable, and then insert into db
                date = value[1]
                permit_no = value[2]
                record_type = value[3]
                description = value[4]
                address = value[5]
                status = value[6]
                print("date: " + date)
                print("status: " + status)
                print("permit no: " + permit_no)
                print("permit type: " + record_type)
                print("address: " + address)
                print("desc: " + description)           
                print("-" * 150)
                cur.execute("""INSERT INTO {0} VALUES('{1}','{2}','{3}','{4}','{5}','{6}');
                """.format(
                        table_name,
                        date,
                        permit_no,
                        record_type,
                        description,
                        address,
                        status,
                ))
                conn.commit()
        odd_rows = soup.find_all("tr", class_="ACA_TabRow_Odd ACA_TabRow_Odd_FontSize")
        for row in odd_rows:
            td = row.find_all('td')
            value = [t.get_text().replace("\n", "").replace("'", "") for t in td]
            if value:
                # instead of just inserting into table with index,  
                # lets assign them to a variable
                date = value[1]
                permit_no = value[2]
                record_type = value[3]
                description = value[4]
                address = value[5]
                status = value[6]
                print("date: " + date)
                print("status: " + status)
                print("permit no: " + permit_no)
                print("permit type: " + record_type)
                print("address: " + address)
                print("desc: " + description)           
                print("-" * 150)
                cur.execute("""INSERT INTO {0} VALUES('{1}','{2}','{3}','{4}','{5}','{6}');
                """.format(
                        table_name,
                        date,
                        permit_no,
                        record_type,
                        description,
                        address,
                        status,
                ))
                conn.commit()
        
        #iterate over all pages by clicking the next button
        try:
            next_page_element = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='{}']".format('Next >'))))
        except Exception as ex:
            our_exception = "An exception of type {0} occured."
            message = our_exception.format(type(ex).__name__)
            print(message)
            break
        next_page_element.click()
        def next_page(driver):
            located_element = driver.find_element_by_xpath("//span[text()='{}']".format(pageno)).get_attribute('class')
            return 'SelectedPageButton font11px' in located_element
        wait = WebDriverWait(driver, 30)
        wait.until(next_page)
        pageno += 1

if __name__ == "__main__":
    driver = init_driver()
    scrape = scrape(driver,
                   'electric', 
                   '01/01/2017',
                   '04/04/2017')
    driver.quit()

