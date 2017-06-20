'''
	script to extract data from finviz.com
'''

from bs4 import BeautifulSoup
import re
import sqlite3
import urllib.request, urllib.error, urllib.parse
from pprint import pprint

conn = sqlite3.connect("python_meetup.sqlite")
cursor = conn.cursor()
table_name = "market_cap"
cursor.execute("DROP TABLE IF EXISTS " + table_name)
cursor.execute("""
	CREATE TABLE {} (
		no integer,
		ticket varchar(10),
		company varchar(255),
		sector varchar(255),
		industry varchar(255),
		country varchar(255),
		market_cap float(4),
		pe float(4),
		price float(4),
		change float(4),
		volume integer
	);
""".format(table_name))
conn.commit()

def get_table_headers():
	url = "http://finviz.com/screener.ashx?v=111&f=cap_nano,sec_healthcare&r=1"
	content = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(content)
	table_headers = []
	for th in soup.select(".table-top"):
		table_headers.append(th.get_text().replace(".", ""))
	ticker = soup.select(".table-top-s")
	table_headers.insert(1, ticker[0].get_text())
	return table_headers


def get_rows_from_soup(soup, table_headers):
	table_row_data = []
	count = 0
	row_data = {}
	for tr in soup.select(".screener-body-table-nw"):
		row_data[table_headers[count]] = tr.get_text()
		count += 1
		if count >= len(table_headers):
			count = 0
			table_row_data.append(row_data)
			row_data = {}
	return table_row_data


def get_data():
	headers = get_table_headers()
	mysite = 'www.imdavemorrison.com'
	initial_number = 1
	while mysite == 'www.imdavemorrison.com':
		url = "http://www.finviz.com/screener.ashx?v=111&f=cap_nano,sec_healthcare&r={}".format(
			initial_number
		)
		content = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(content)
		data = get_rows_from_soup(soup, headers)
		for row in data:
			print(row['No'])
			print(row['Ticker'])
			print(row['Company'])
			print(row['Sector'])
			print(row['Industry'])
			print(row['Country'])
			print(row['Market Cap'][:-1])
			print("") if row['P/E'] == "-" else print(row['P/E'])
			print(row['Price'])
			print(row['Change'][:-1])
			print(row['Volume'].replace(',', ""))
			print("-" * 100)
			cursor.execute('INSERT INTO market_cap VALUES(?,?,?,?,?,?,?,?,?,?,?)',(
					row['No'],
					row['Ticker'],
					row['Company'],
					row['Sector'],
					row['Industry'],
					row['Country'],
					row['Market Cap'][:-1],
					"" if row['P/E'] == "-" else row['P/E'],
					row['Price'],
					row['Change'][:-1],
					row['Volume'].replace(',', ""),
				))
			conn.commit()			
		initial_number += 20
		if not re.findall(b"<b>next</b>", content):
			mysite = 'imdavemorrison'

get_data()

