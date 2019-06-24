import os  
import time
import pandas as pd
import numpy as np
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException

importersweb = 'https://www.xxxxxxxxxxxxxxxxxxxxxxxx'
listcountry = "//a[@id='details-panel3-lnk']"
china = "//option[contains(text(),'China')]"
viewcountry = "//input[@id='viewCountry']"
recordselect = "//select[@name='wb-auto-1_length']"
hundrecord = "//option[contains(text(),'100')]"
lastpage = "/html[1]/body[1]/main[1]/div[2]/form[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/span[1]/a[6]"
nextpage = "//a[@id='wb-auto-1_next']"

chrome_options = Options()  
chrome_options.add_argument("--headless")
driver = webdriver.Chrome()#options=chrome_options)#executable_path=os.path.abspath("chromedriver"), options=chrome_options)  
driver.maximize_window()
driver.get(importersweb)

homepage = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, listcountry)))
homepage.click()

chinatab = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, china)))
chinatab = driver.find_element_by_xpath(china)
chinatab.location_once_scrolled_into_view
chinatab.click()

importchina = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, viewcountry)))
importchina = driver.find_element_by_xpath(viewcountry)
importchina.location_once_scrolled_into_view
importchina.click()

dropdown = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, recordselect)))
dropdown = driver.find_element_by_xpath(recordselect)
dropdown.click()
hundre = driver.find_element_by_xpath(hundrecord)
hundre.click()

def pagerecords(count):
    companyname = []
    city = []
    province = []
    postalcode = []
    for i in range(1,int(count)):
        comname = "//tbody//tr[%i]//td[1]"%i
        cityname = "//tbody//tr[%i]//td[2]"%i
        provin = "//tbody//tr[%i]//td[3]"%i
        poscode = "//tbody//tr[%i]//td[4]"%i
        cn = driver.find_element_by_xpath(comname)
        ct = driver.find_element_by_xpath(cityname)
        pr = driver.find_element_by_xpath(provin)
        pc = driver.find_element_by_xpath(poscode)
        #cn.location_once_scrolled_into_view
        companyname.append(cn.text)
        city.append(ct.text)
        province.append(pr.text)
        postalcode.append(pc.text)
        codataframe = pd.DataFrame(np.column_stack([companyname,city,province,postalcode]), columns=['Company name','City','Province','Postal code'])
    return codataframe
    
pageall = driver.find_element_by_xpath(lastpage).text
pageall = str(pageall)
p = pageall.split('\n')[1]

def changepage(p):
    result = pd.DataFrame(columns=['Company name','City','Province','Postal code'])
    newpage = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, recordselect)))
    for i in range(1,int(p)+1):
        count = len(driver.find_elements_by_xpath('//tr'))
        pre = pagerecords(count)
        frames = [result, pre]
        result = pd.concat(frames)
        nextp = driver.find_element_by_xpath(nextpage)
        nextp.location_once_scrolled_into_view
        try:
            driver.execute_script("return arguments[0].scrollIntoView(true);", nextp)
            nextp.click()
            print("It's the %i page"%i)
        except ElementNotVisibleException:
            print("It's the last page")  
        time.sleep(1)
    return result
        
resultdf = changepage(p)

resultdf.to_excel('canada-chinese-importers.xlsx', header=True, index=False)
