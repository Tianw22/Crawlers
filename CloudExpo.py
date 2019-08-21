from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import requests
import pandas as pd
from pandas.core.frame import DataFrame

cloudexpoweb = 'https://cloudexpo2018.sched.com/directory/attendees'
pagetotal = int(21)

chrome_options = Options()  
chrome_options.add_argument("--headless")
driver = webdriver.Chrome()#options=chrome_options)#executable_path=os.path.abspath("chromedriver"), options=chrome_options)  
driver.maximize_window()
driver.get(cloudexpoweb)

def getncp(i):
    name = "/html[1]/body[1]/div[3]/div[1]/div[2]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[%i]/h2[1]/a[1]"%i
    company = "/html[1]/body[1]/div[3]/div[1]/div[2]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[%i]/div[1]/div[1]"%i
    position = "/html[1]/body[1]/div[3]/div[1]/div[2]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[%i]/div[1]/div[2]"%i
    namestr = driver.find_element_by_xpath(name).text
    driver.find_element_by_xpath(name).location_once_scrolled_into_view
    namerecord = str(namestr)
    comstr = driver.find_element_by_xpath(company).text
    comrecord = str(comstr)
    posstr = driver.find_element_by_xpath(position).text
    posrecord = str(posstr)
    return namerecord,comrecord,posrecord

def perpage(pagenum):
    namelist = []
    companylist = []
    positionlist = []
    count = len(driver.find_elements_by_xpath("//div[@class='sched-person']"))
    for i in range(1,int(count)+1):
        person = "//div[@class='sched-person'][%i]"%i
        personloc = driver.find_element_by_xpath(person)
        personloc.location_once_scrolled_into_view
        n,c,p = getncp(i)
        namelist.append(n)
        companylist.append(c)
        positionlist.append(p)
        frames = {"Name" : namelist, "Company" : companylist, "Position" : positionlist}
    return frames

    resultdf = pd.DataFrame(columns=['Name','Company','Position'])

    for i in range(1,int(pagetotal)+1):
        page = "https://cloudexpo2018.sched.com/directory/attendees/%i"%i
        driver.get(page)
        res = perpage(i)
        resdf = pd.DataFrame(res)
        resultdf = pd.concat([resultdf,resdf])

    resultdf.to_excel("cloudexporesult.xlsx")
