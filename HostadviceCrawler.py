#BeautifulSoup and selenium work wonderful together.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re
import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas.core.frame import DataFrame

#If other browers is preferred, download the specific web driver of the brower and add the web driver to PATH.
#Change .Chrome() into the brower will be used.
driver = webdriver.Chrome()
driver.get("https://hostadvice.com/")
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

#Close the alert(advertisement) window
alertwindow1 = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, "//button[@id='onesignal-popover-cancel-button']")))
alertwindow1.click()

#Find the input box of country
elem = driver.find_element_by_xpath("//input[@id='filter-servers-country']")

#Input the country going to be collected
#Tricky to choose from an autocompletion input box.
print("Input the country you want to search: ")
country = input("")
elem.send_keys(country)
time.sleep(1)
elem.send_keys(Keys.ARROW_DOWN)
elem.send_keys(Keys.RETURN)
time.sleep(5)

#Find the total page number
pagenum = driver.find_element_by_xpath("/html[1]/body[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[5]/div[2]/a[2]").text
countryurl = driver.current_url
pagenum = int(pagenum)
#print(pagenum)

#Create two empty lists to store the names and links of the companies
names=[]
links=[]

#Create a clawer that obtain names and domain links of the companies
def hostadvice(driver):
    req = requests.get(url = driver,headers = headers)
    html = req.text
    div_bf = BeautifulSoup(html,'html.parser')
    div = div_bf.find_all('div', class_ = 'text-links')
    a_bf = BeautifulSoup(str(div))
    a_no = a_bf.find_all('a', rel = 'nofollow')
    for each in a_no:
        names.append(each.get('title'))
    #print(names)
    #Get text outside a pair of <> in DOM
    for each in a_no:
        links.append(each.get_text())
    #print(links)
    Total={"Name" : names, "Domain" : links}
    df = DataFrame(Total)
    return df

#Collect names and domains from the first page to the last page.
pagemax = pagenum + 1
for i in range(1,pagemax):
    driver = countryurl
    driver = driver + 'page/%i'%i
    time.sleep(5)
    df = hostadvice(driver)
    df = df.append(df, ignore_index=True)
    i = i + 1
    #print(driver)

#Save results into .csv with the country input.
s = str(country)
df.to_csv('hostadvice%s.csv'%s)
