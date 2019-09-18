import SeleniumLibrary
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

driver = webdriver.Chrome()
driver.maximize_window()

def getlist(pagelink):
    driver.get(pagelink)
    wait = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH, "//tr[4]//td[2]")))
    countvert = len(driver.find_elements_by_xpath("//tr//td[1]"))
    asrank = []
    asnum = []
    orgname = []
    orglink = []
    nation = []
    for i in range(4,int(countvert)+4):
        
        rank = driver.find_element_by_xpath("//tr[%i]//td[1]"%i).text
        asrank.append(rank)
        num = driver.find_element_by_xpath("//tr[%i]//td[2]"%i).text
        asnum.append(num)
        
        try:
            name = driver.find_element_by_xpath("//tr[%i]//td[3]//a[1]"%i).text
            orgname.append(name)
        except NoSuchElementException:
            name = "unknown"
            orgname.append(name)
        
        try:
            link = driver.find_element_by_xpath("//tr[%i]//td[3]/a[@href]"%i).get_attribute("href")
            orglink.append(link)
        except NoSuchElementException:
            link = "unknown"
            orglink.append(link)
            
        try:
            flag = driver.find_element_by_xpath("//tr[%i]//td[4]//span[@class]"%i).get_attribute("class")
            nation.append(flag) 
        except NoSuchElementException:
            flag = "unknown"
            nation.append(flag) 
            
    dic = {"AS Rank" : asrank, "AS Number" : asnum, "Org Name" : orgname, "Org Link" : orglink, "Nation" : nation}
    df = pd.DataFrame(dic)
    return df
    
for i in range(1,1650):
    #print(i)
    website = "https://asrank.caida.org/asns?page_number=%i&page_size=40&sort=rank"%i
    df = getlist(website)
    df.to_csv('aslist-csv.csv',mode='a',header=False)
