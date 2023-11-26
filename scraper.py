# Import necessary libraries
from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os
import sys
import csv
counties = {"harjumaa":1,"tartumaa":12}
cities = {"tallinn":1061,"tartu":1063}
startyear = 2007
endyear = 2023
startmonth = 5
endmonth = 11
url = f"""https://www.kv.ee/et/hinnastatistika?
graph_version=2&show_compare_line=1&deal_type=1&
start_year={startyear}&start_month={startmonth}&end_year={endyear}&end_month={endmonth}&
county1={counties["harjumaa"]}&parish1={cities["tallinn"]}&city1=0&county2={counties["tartumaa"]}&parish2={cities["tartu"]}&city2=0&
graph_version=2&show_compare_line=1&deal_type=1&start_year={startyear}&
start_month={startmonth}&end_year={endyear}&end_month={endmonth}&county1={counties["harjumaa"]}&parish1={cities["tallinn"]}&
city1=0&county2={counties["tartumaa"]}&parish2={cities["tartu"]}&city2=0&graph_version=2&
show_compare_line=1&deal_type=1&start_year={startyear}&start_month={startmonth}&
end_year={endyear}&end_month={endmonth}&county{counties["harjumaa"]}=1&parish1={cities["tallinn"]}&city1=0&county2={counties["tartumaa"]}&
parish2={cities["tartu"]}&city2=0"""


os.environ['PATH'] = f'{os.environ["PATH"]};C:\\Webdrivers\\'


driver = webdriver.Firefox()
# Specify the URL of the webpage you want to scrape
driver.get(url)
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id='onetrust-reject-all-handler']"))).click()
sleep(1)
r = driver.page_source
driver.close
# Send HTTP request to the specified URL and save the response from server in a response object called r
#r = requests.get(url)

# Create a BeautifulSoup object and specify the parser library at the same time
soup = BeautifulSoup(r, 'html.parser')
table = soup.find("table", class_="table-striped")

# Create a list to store the data
data = []
data_headers = ["date",f"price-{cities['tallinn']}",f"Advertisements-{cities['tallinn']}",f"Actives-{cities['tallinn']}",f"price-{cities['tartu']}",f"Advertisements-{cities['tartu']}",f"Actives-{cities['tartu']}"]
data.append(data_headers)
# Find all the rows of the table
rows = table.find_all('tr')

for row in rows:
    # Find all columns in each row
    cols = row.find_all('td')
    
    # Get the text from each column
    cols = [col.text for col in cols]
    
    # Add the columns to the data array
    data.append(cols)

# Print the data array

# Open (or create) a CSV file with write permissions ('w')
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write each row to the CSV
    for row in data:
        writer.writerow(row)