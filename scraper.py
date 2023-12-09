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
os.environ['PATH'] = f'{os.environ["PATH"]};C:\\Webdrivers\\'
driver = webdriver.Firefox()
driver.get("https://www.kv.ee/et/hinnastatistika")
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id='onetrust-reject-all-handler']"))).click()
sleep(1)
    
def create_url(startyear, startmonth, endyear, endmonth,county, parish,city):
    url = f"https://www.kv.ee/et/hinnastatistika?graph_version=2&show_compare_line=1&deal_type=1&start_year={startyear}&start_month={startmonth}&end_year={endyear}&end_month={endmonth}&county1={county}&parish1={parish}&city1={city}&county2={county}&parish2={parish}&city2={city}"
    return url

def get_data(url,driver,previous_data,city,district):
    driver.get(url)
    sleep(2)
    r = driver.page_source
    soup = BeautifulSoup(r, 'html.parser')
    table = soup.find("table", class_="table-striped")

    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text for col in cols]
        if len(cols)<1: continue
        date = cols[0].replace(".", "-")
        toadd = [date,city,district]
        toadd.extend(cols[1:])
        previous_data.append(toadd)

    return previous_data

counties = {"harjumaa":1,"tartumaa":12}
cities = {"Tallinn":1061,"Tartu":1063}
startyear = 2007
endyear = 2023
startmonth = 1
endmonth = 12
tlncities = {"Tallinn":0,"Haabersti":1001,"Kesklinn":1003,"Kristiine":1004,"Lasnamäe":1006,"Mustamäe":1007,"Nõmme":1008,"Pirita":1010,"Põhja-Tallinn":1011,"Vanalinn":5700,"Kadriorg":5701}
trtcities = {"Tartu":0,"Haage":1334,"Ilmatsalu küla":1530,"Ilmatsalu alevik":1531,"Kandiküla":1857,"Kardla":1887,"Märja":3317,"Pihva":3760,"Rahinge":4058,"Rõhu":4288,"Tartu linn":4820,
             "Tähtvere":5036,"Tüki":5053,"Vorbuse":5515,"Maarjamõisa":5702,"Raadi-Kruusamäe":5703,"Karlova":5704,"Kesklinn":5705,"Ihaste":5706,"Jaamamõisa":5707,"Annelinn":5708,"Veeriku":5709,
             "Ülejõe":5710,"Vaksali":5711,"Variku":5712,"Tammelinn":5713,"Tähtvere":5714,"Ränilinn":5715,"Supilinn":5716,"Ropka":5717,"Ropka tööstusrajoon":5718}
firstcity = ""
secondcity = ""


indx = 0
data = [["date","city","district","price", "advertisements","actives"]]
for tln in tlncities.keys():
    url = create_url(startyear, startmonth, endyear, endmonth, counties["harjumaa"],cities["Tallinn"],tlncities[tln])
    data = get_data(url,driver,data,"Tallinn",tln)
        
for trt in trtcities.keys():
    url = create_url(startyear, startmonth, endyear, endmonth, counties["tartumaa"],cities["Tartu"],trtcities[trt])
    data = get_data(url,driver,data,"Tartu",trt)
driver.close
    
with open('data2007_1-2023_12.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for row in data:
        writer.writerow(row)